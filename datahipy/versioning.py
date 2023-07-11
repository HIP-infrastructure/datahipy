# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Methods supporting versioning of BIDS and Collaborative project datasets."""

import datalad


def create_tag(dataset_dir, tag, message):
    """Create a version tag on a dataset managed by Git/Datalad.

    Parameters
    ----------
    dataset_dir : str
        Absolute path to the dataset directory.

    tag : str
        Tag in the format.

    message : str
        Message to be associated with the tag.

    Returns
    -------
    res : datalad.utils.Result
        Result of the Datalad save operation.
    """
    # Create a tag on the dataset
    res = datalad.api.save(
        dataset=dataset_dir,
        message=message,
        version_tag=tag,
    )
    print(f"Tag creation results: {res}")
    return res


def get_tags(dataset_dir):
    """Get the list of tags of a dataset managed by Git/Datalad via subprocess.

    Parameters
    ----------
    dataset_dir : str
        Absolute path to the dataset directory.

    Returns
    -------
    tags : list
        List of tags of the dataset.
    """
    tags = datalad.support.gitrepo.GitRepo(dataset_dir).get_tags()
    print(f"Tags: {tags}")
    return tags


def checkout_tag(dataset_dir, tag):
    """Checkout a specific tag of a dataset managed by Git/Datalad via subprocess.

    Parameters
    ----------
    dataset_dir : str
        Absolute path to the dataset directory.

    tag : str
        Tag to checkout.

    Returns
    -------
    res : datalad.utils.Result
        Result of the Datalad checkout operation.
    """
    # Checkout a specific tag of the dataset to a new eponymous branch
    datalad.support.gitrepo.GitRepo(dataset_dir).checkout(
        name=f"tags/{tag}",
        options=["-b {tag}", "--force"],
    )
