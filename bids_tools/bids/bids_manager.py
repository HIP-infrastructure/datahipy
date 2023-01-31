# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Utility functions to modify BIDS datasets created using `BIDS_Manager`."""

from os import path as op
import json


def correct_bids_ieeg_json(bids_ieeg_json):
    """Correct BIDS iEEG json file.

    Parameters
    ----------
    bids_ieeg_json : str
        Path to the BIDS iEEG json file.

    Returns
    -------
    bids_ieeg_json_content : dict
        Corrected content overwritten to the BIDS iEEG json file.

    """
    # Load the BIDS iEEG json file
    with open(bids_ieeg_json, "r") as f:
        bids_ieeg_json_content = json.load(f)

    # Correct the BIDS iEEG json file
    # Remove AcquisitionDate field as additional fields are not allowed
    if "AcquisitionDate" in bids_ieeg_json_content.keys():
        del bids_ieeg_json_content["AcquisitionDate"]

    # Save the corrected BIDS iEEG json file
    with open(bids_ieeg_json, "w") as f:
        json.dump(bids_ieeg_json_content, f, indent=4)

    return bids_ieeg_json_content
