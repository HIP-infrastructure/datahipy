# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to retrieve participant-level information from a BIDS dataset."""

import pandas as pd
from os import path as op
from datahipy.bids.const import (
    VALID_EXTENSIONS,
    BIDS_ENTITY_MAP,
    BIDSJSONFILE_DATATYPE_KEY_MAP,
    BIDSTSVFILE_DATATYPE_KEY_MAP,
)


def get_subject_bidsfile_info(bids_dir, **kwargs):
    """Return a list of dictionaries with BIDS file information for a given subject.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    kwargs : dict
        Dictionary of arguments key/value to pass to the pybids BIDSLayout.get() function.

    Returns
    -------
    subject_info : list
        List of dictionaries with BIDS file information for a given subject.
    """
    # Import the required functions
    from datahipy.bids.dataset import create_bids_layout
    from datahipy.bids.electrophy import get_channels_info

    # Create a pybids representation of the dataset
    layout = create_bids_layout(bids_dir)
    # Get the list of files for the given subject (and session, task and run if provided)
    files = layout.get(**kwargs)
    # Initialize the dictionary to be returned
    subject_bids_file_info = []
    # Loop over the found files
    for file in files:
        # Initialize the dictionary with the file information
        file_info = {}
        # Skip the json and tsv files
        if (file.entities["extension"] in [".json", ".tsv"]) or (
            file.entities["extension"] not in VALID_EXTENSIONS
        ):
            continue
        # Extract the datatype
        file_info["datatype"] = file.entities["datatype"]
        # Extract the modality from the suffix
        file_info["modality"] = file.entities["suffix"]
        file_info["extension"] = file.entities["extension"]
        # Extract all the "proper" BIDS entities
        for key in file.entities:
            if key in BIDS_ENTITY_MAP.keys():
                file_info[BIDS_ENTITY_MAP[key]] = file.entities[key]
        # Extract the relative path of the file
        file_info["fileLoc"] = file.relpath
        # Extract the file metadata from the BIDS json sidecar file
        file_metadata = layout.get_metadata(file.path)
        if file_metadata:
            file_info[
                BIDSJSONFILE_DATATYPE_KEY_MAP[file_info["datatype"]]
            ] = file_metadata
            del file_metadata
        # Extract the channel information from the channels tsv file for EEG, MEG and iEEG
        if file_info["datatype"] in ["eeg", "meg", "ieeg"]:
            file_info[
                BIDSTSVFILE_DATATYPE_KEY_MAP[file_info["datatype"]]
            ] = get_channels_info(
                file.path.split(f'_{file_info["datatype"]}')[0] + "_channels.tsv"
            )
        # Add the file information to the list
        subject_bids_file_info.append(file_info)
    # Return the list of dictionaries
    return subject_bids_file_info


def get_participants_info(bids_dir):
    """Update the input `dataset_desc` dictionary with information from the `participants.tsv` file.

    Parameters
    ----------
    dataset_desc : dict
        Input dictionary with the dataset content to be indexed.

    bids_dir : str
        Path to the BIDS dataset.

    Returns
    -------
    dataset_desc : dict
        Updated dictionary with the dataset content to be indexed.
    """
    participants_info = {}
    # Load the participants.tsv file to extract information about participants
    try:
        participants_df = pd.read_csv(
            op.join(bids_dir, "participants.tsv"),
            sep="\t",
            header=0,
            na_filter=False,
        )
    except pd.errors.EmptyDataError:
        participants_df = pd.DataFrame()
    # Get min and max age of participants
    if "age" in participants_df.keys():
        participants_info["AgeMin"] = f'{participants_df["age"].min()}'
        participants_info["AgeMax"] = f'{participants_df["age"].max()}'
    else:
        participants_info["AgeMin"] = None
        participants_info["AgeMax"] = None
    participants_info["ParticipantsCount"] = len(participants_df.index)
    participants_info["ParticipantsGroups"] = (
        list(participants_df["group"].unique())
        if "group" in participants_df.keys()
        else [None]
    )
    # Store content of participants.tsv as a dictionary
    participants_info["Participants"] = participants_df.to_dict(orient="records")
    del participants_df
    return participants_info
