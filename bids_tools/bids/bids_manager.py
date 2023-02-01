# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Utility functions to modify BIDS datasets created using `BIDS_Manager`."""

import os
import json

from bids_tools.bids.dataset import create_bids_layout


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


def post_import_bids_refinement(bids_dir):
    """Refine BIDS files after import.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    Returns
    -------
    None

    """
    # Correct BIDS iEEG json files
    layout = create_bids_layout(bids_dir)
    ieeg_json_files = layout.get(suffix="ieeg", extension="json")
    for ieeg_json_file in ieeg_json_files:
        print(f"> Correcting {ieeg_json_file.path}...")
        correct_bids_ieeg_json_content = correct_bids_ieeg_json(
            ieeg_json_file.path
        )
        print(f"  .. New content: {correct_bids_ieeg_json_content}")
    # Remove scans.tsv files
    scans_files = layout.get(suffix="scans", extension="tsv")
    for scans_file in scans_files:
        print(f"> Removing {scans_file.path}...")
        os.remove(scans_file.path)
    # Remove events.tsv files if they consist only of one line (i.e., header)
    events_files = layout.get(suffix="events", extension="tsv")
    for events_file in events_files:
        with open(events_file.path, "r") as f:
            events_file_content = f.readlines()
        if len(events_file_content) == 1:
            print(f"> Removing {events_file.path} which is empty...")
            os.remove(events_file.path)
