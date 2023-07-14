# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Methods supporting versioning of BIDS and Collaborative project datasets."""

import os
import json
from sre_constants import SUCCESS

import datalad
from datalad.support.gitrepo import GitRepo

from datahipy.bids.version import create_bids_changes_tag_entry, update_bids_changes


TAG_EXCEPTIONS = ["master", "main", "HEAD"]


def validate_tag(tag, discard_exceptions=False):
    """Validate a tag.

    Parameters
    ----------
    tag : str
        Tag to validate.

    discard_exceptions : bool
        If True, discard the exceptions listed by `TAG_EXCEPTIONS`
        and return False.

    Returns
    -------
    bool
        True if the tag is valid, False otherwise.
    """
    # Check if the tag is in the format X.Y.Z
    # where X, Y, and Z are integers via regex
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    try:
        if not all(0 <= int(n) < 256 for n in tag.split(".")):
            return False
    except ValueError:
        if (not discard_exceptions) and (tag in TAG_EXCEPTIONS):
            return True
        else:
            return False
    return True


def create_tag(input_data):
    """Create a version tag on a dataset managed by Git/Datalad.

    **Note:** The tag is created on a Datalad dataset, not on a specific file.
    If the dataset is a BIDS dataset, the tag will be created only on this dataset.
    If the dataset is a Collaborative Project, the tag will be created recursively on
      the project dataset and on the nested BIDS dataset of the project.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the input data for the command
        in the format::

            {
                "path": "/path/to/dataset",
                "type": "bids",  # or "project"
                "tag": "1.0.0",
                "changes_list": ["Change 1", "Change 2"]
            }
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)
    print(f"Create tag {input_data['tag']} for dataset {input_data['path']}...")

    # Check if the tag is valid
    if not validate_tag(input_data["tag"], discard_exceptions=True):
        raise ValueError(
            f"Impossible to create tag {input_data['tag']}. The format is not valid. "
            "Please use the format X.Y.Z, where X, Y, and Z are integers."
        )
    # Check if the tag already exists
    if input_data["tag"] in [
        tag_dict["name"] for tag_dict in GitRepo(input_data["path"]).get_tags()
    ]:
        raise ValueError(
            f"Impossible to create tag {input_data['tag']}. "
            f"Tag {input_data['tag']} already exists."
        )
    # Create the tag message based on tag, date, and list of changes
    changes_tag_entry = create_bids_changes_tag_entry(
        tag=input_data["tag"],
        changes_list=input_data["changes_list"],
    )
    if input_data["type"] == "bids":
        bids_dir = input_data["path"]
    elif input_data["type"] == "project":
        bids_dir = os.path.join(input_data["path"], "inputs", "bids-dataset")
    # Update the CHANGES file with the generated tag text entry
    update_bids_changes(
        bids_dir=bids_dir,
        changes_tag_entry=changes_tag_entry,
    )
    # Create a tag on the dataset
    save_params = {
        "dataset": input_data["path"],
        "message": "".join(changes_tag_entry),
        "version_tag": input_data["tag"],
        "recursive": True,
    }
    datalad.api.save(**save_params)
    print(SUCCESS)


def get_tags(input_data, output_file):
    """Get the list of tags of a dataset managed by Git/Datalad via subprocess.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the input data for the command
        in the format::

            {
                "path": "/path/to/dataset",
            }

    output_file : str
        Absolute path to the output JSON file containing the tags
        in the format::

            {
                "path": "/path/to/dataset",
                "tags": ["1.0.0", "1.0.1", "1.1.0"]
            }
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)

    tags = [tag_dict["name"] for tag_dict in GitRepo(input_data["path"]).get_tags()]
    dict_tags = {
        "path": input_data["path"],
        "tags": tags,
    }

    print(f"Tags: {tags}")
    # Save the tags to a JSON file
    with open(output_file, "w") as f:
        json.dump(dict_tags, f)
    print(SUCCESS)


def checkout_tag(input_data):
    """Checkout a specific tag of a dataset managed by Git/Datalad via subprocess.

    **Note:** The master / main branch / or the HEAD can also be checked out by specifying
      "master" / "main" / "HEAD" for the tag value.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the input data for the command
        in the format::

            {
                "path": "/path/to/dataset",
                "tag": "1.0.0",
            }
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)
    # Check of the tag format is valid
    if not validate_tag(input_data["tag"]):
        raise ValueError(
            f"Impossible to checkout tag {input_data['tag']}. The format is not valid. "
            "Please use the format X.Y.Z, where X, Y, and Z are integers, or "
            "specify 'master' / 'main' to checkout the master / main branch."
        )
    # Set the name and options for tag / branch checkout
    if input_data["tag"] not in TAG_EXCEPTIONS:
        name = f"tags/{input_data['tag']}"
        checkout_opts = ["-b", f"{input_data['tag']}", "--force"]
    else:
        name = input_data["tag"]
        checkout_opts = ["--force"]
    # Checkout a specific tag of the dataset to a new eponymous branch
    # or checkout the master / main branch / HEAD
    GitRepo(input_data["path"]).checkout(
        name=name,
        options=checkout_opts,
    )
    print(SUCCESS)


def get_latest_tag(path):
    """Get the latest tag of a dataset managed by Git/Datalad.

    Parameters
    ----------
    path : str
        Absolute path to the dataset.

    Returns
    -------
    str
        The latest tag of the dataset.
    """
    tags = [tag_dict["name"] for tag_dict in GitRepo(path).get_tags()]
    tags.sort(key=lambda s: list(map(int, s.split("."))), reverse=True)
    if len(tags) == 0:
        return "0.0.0"
    return tags[0]


def increment_tag(tag, level):
    """Increment a version tag by a specific level.

    Parameters
    ----------
    tag : str
        Version tag to increment in the format X.Y.Z, where X, Y, and Z are integers.

    level : str
        Level to increment. Can be "major", "minor", or "patch".

    Returns
    -------
    str
        The incremented tag.
    """
    if not validate_tag(tag, discard_exceptions=True):
        raise ValueError(
            f"Impossible to increment tag {tag}. The format is not valid. "
            "Please use the format X.Y.Z, where X, Y, and Z are integers."
        )
    tag = tag.split(".")
    if level == "major":
        tag[0] = str(int(tag[0]) + 1)
        tag[1] = "0"
        tag[2] = "0"
    elif level == "minor":
        tag[1] = str(int(tag[1]) + 1)
        tag[2] = "0"
    elif level == "patch":
        tag[2] = str(int(tag[2]) + 1)
    return ".".join(tag)
