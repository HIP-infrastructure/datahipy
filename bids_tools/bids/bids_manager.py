# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to modify BIDS datasets created using `BIDS_Manager`."""

import os
import re
import json

from bids_tools.bids.dataset import create_bids_layout


def post_import_bids_refinement(bids_dir):
    """Refine BIDS files after import.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.
    """
    # Create BIDSLayout object representation
    layout = create_bids_layout(bids_dir)
    # Correct BIDS iEEG json files
    correct_bids_ieeg_json_files(layout)
    # Remove scans.tsv files
    remove_scans_tsv_files(layout)
    # Remove events.tsv files if they consist only of one line (i.e., header)
    clean_empty_events_tsv_files(layout)
    # Correct format of some fields expecting list type in dataset_description.json
    ensure_list_fields_in_dataset_description(
        bids_dir=bids_dir, fields=["Funding", "ReferencesAndLinks"]
    )
    # Rename files with run-0X to run-X
    correct_run_index_filename(layout)


def correct_bids_ieeg_json_files(layout):
    """Correct BIDS iEEG json files.

    Parameters
    ----------
    layout : bids.BIDSLayout
        BIDSLayout object representation of the BIDS dataset.
    """
    ieeg_json_files = layout.get(suffix="ieeg", extension="json")
    for ieeg_json_file in ieeg_json_files:
        print(f"> Correcting {ieeg_json_file.path}...")
        correct_bids_ieeg_json_content = correct_bids_ieeg_json_file(
            ieeg_json_file.path
        )
        print(f"  .. New content: {correct_bids_ieeg_json_content}")


def correct_bids_ieeg_json_file(bids_ieeg_json):
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


def remove_scans_tsv_files(layout):
    """Remove scans.tsv files.

    Parameters
    ----------
    layout : bids.BIDSLayout
        BIDSLayout object representation of the BIDS dataset.
    """
    scans_files = layout.get(suffix="scans", extension="tsv")
    for scans_file in scans_files:
        print(f"> Removing {scans_file.path}...")
        os.remove(scans_file.path)


def clean_empty_events_tsv_files(layout):
    """Remove empty events.tsv files.

    Parameters
    ----------
    layout : bids.BIDSLayout
        BIDSLayout object representation of the BIDS dataset.
    """
    events_files = layout.get(suffix="events", extension="tsv")
    for events_file in events_files:
        with open(events_file.path, "r") as f:
            events_file_content = f.readlines()
        if len(events_file_content) == 1:
            print(f"> Removing {events_file.path} which is empty...")
            os.remove(events_file.path)


def ensure_list_fields_in_dataset_description(bids_dir, fields):
    """Ensure that some fields are list type in dataset_description.json.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.
    fields : list of str
        List of fields to ensure are list type.
    """
    # Load dataset_description.json
    dataset_desc_path = os.path.join(bids_dir, "dataset_description.json")
    with open(dataset_desc_path, "r") as f:
        dataset_desc = json.load(f)
    # Ensure that some fields are list type
    for field in fields:
        if field in dataset_desc.keys():
            if not isinstance(dataset_desc[field], list):
                dataset_desc[field] = [dataset_desc[field]]
    # Overwrite dataset_description.json
    with open(dataset_desc_path, "w") as f:
        json.dump(dataset_desc, f, indent=4)


def correct_run_index_filename(layout):
    """Correct run index in BIDS filenames.

    Parameters
    ----------
    layout : bids.BIDSLayout
        BIDSLayout object representation of the BIDS dataset.
    """
    for filename in layout.get(return_type="file"):
        if re.search(r"_run-0[0-9]_", os.path.basename(filename)):
            run_num = int(
                re.search(r"_run-0([0-9])_", os.path.basename(filename)).group(
                    1
                )
            )
            new_filename = os.path.join(
                os.path.dirname(filename),
                os.path.basename(filename).replace(
                    f"run-0{run_num}", f"run-{run_num}"
                ),
            )
            print(f"> Renaming {filename} to {new_filename}...")
            os.rename(filename, new_filename)
