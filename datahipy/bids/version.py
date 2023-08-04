# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to retrieve version related information from a BIDS dataset."""

import os
from datetime import date
from packaging import version
import datalad.api
from datahipy.bids.const import BIDS_VERSION


def determine_bids_schema_version(dataset_desc):
    """Determine the BIDS schema version of the BIDS dataset against which it will be validated.

    Parameters
    ----------
    dataset_desc : dict
        Content of the dataset_description.json file.

    Returns
    -------
    bids_schema_version : str
        BIDS schema version against which the BIDS dataset will be validated.
    """
    if "BIDSVersion" in dataset_desc.keys():
        try:
            if version.parse(dataset_desc["BIDSVersion"]) < version.parse("1.6.0"):
                bids_schema_version = "v1.6.0"
            elif dataset_desc["BIDSVersion"] in ["1.6.0", "1.7.0"]:
                bids_schema_version = "v" + dataset_desc["BIDSVersion"]
            elif version.parse(dataset_desc["BIDSVersion"]) > version.parse("1.7.0"):
                bids_schema_version = "v1.7.0"
        except Exception as e:
            print(
                f"Error parsing BIDSVersion: {e}"
                f"Using default BIDS version: {BIDS_VERSION}"
            )
            bids_schema_version = BIDS_VERSION
    else:
        bids_schema_version = BIDS_VERSION
    return bids_schema_version


def create_bids_changes_tag_entry(tag, changes_list):
    """Create a release text block entry to be added to the CHANGES file of a BIDS dataset.

    Parameters
    ----------
    tag : str
        Tag of the dataset.

    changes_list : list
        List of changes to add to the `CHANGES` file.

    Returns
    -------
    list
        List of lines to be written to the `CHANGES` file.
    """
    return [
        f"{tag} {date.today().strftime('%Y-%m-%d')}\n",
        "\n\t- " + "\n\t- ".join(changes_list),
        "\n\n",
    ]


def update_bids_changes(bids_dir, changes_tag_entry):
    """Append a new release text block to the top to the `CHANGES` file of a BIDS dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    tag : str
        Tag of the dataset.

    changes_tag_entry : list
        List of lines to be written to the `CHANGES` file.
    """
    # Read the current content of the CHANGES file
    with open(os.path.join(bids_dir, "CHANGES"), "r") as f:
        content = f.readlines()
    # Create a new CHANGES file with the new release text block at the top
    with open(os.path.join(bids_dir, "CHANGES"), "w") as f:
        f.writelines(changes_tag_entry + content)


def manage_bids_dataset_with_datalad(bids_dir):
    """Create a Datalad dataset out of an existing BIDS dataset not Datalad-managed yet."""
    print(f"Initializing Datalad dataset at {bids_dir}...")
    # Initialize the BIDS dataset as a Datalad-managed dataset
    create_params = {
        "dataset": bids_dir,
        "cfg_proc": ["text2git", "bids"],
        "force": True,  # Enforce dataset creation in a non-empty directory
    }
    datalad.api.create(**create_params)
