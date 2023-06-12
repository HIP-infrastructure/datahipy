# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to retrieve version related information from a BIDS dataset."""

from packaging import version
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
            if version.parse(dataset_desc["BIDSVersion"]) < version.parse(
                "1.6.0"
            ):
                bids_schema_version = "v1.6.0"
            elif dataset_desc["BIDSVersion"] in ["1.6.0", "1.7.0"]:
                bids_schema_version = "v" + dataset_desc["BIDSVersion"]
            elif version.parse(dataset_desc["BIDSVersion"]) > version.parse(
                "1.7.0"
            ):
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
