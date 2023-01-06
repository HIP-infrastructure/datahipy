# Copyright (C) 2022, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.
"""Utility function using pybids."""

import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pkg_resources import resource_filename

import json
import pandas as pd
from sre_constants import SUCCESS
from bids import BIDSLayout
from bids_tools.bids.const import (
    BIDS_VERSION,
    BIDS_ENTITY_MAP,
    BIDSJSONFILE_DATATYPE_KEY_MAP,
    BIDSTSVFILE_DATATYPE_KEY_MAP,
    VALID_EXTENSIONS,
)


NUM_THREADS = os.cpu_count() - 1 if os.cpu_count() > 1 else 1


def create_bids_layout(container_dataset_path=None, **kwargs):
    """Create a pybids representation of a BIDS dataset.

    Parameters
    ----------
    container_dataset_path : str
        Path to the BIDS dataset.

    kwargs : dict
        Dictionary of arguments key/value to pass to the pybids BIDSLayout function.

    Returns
    -------
    layout : pybids.BIDSLayout
        Pybids representation of the BIDS dataset.
    """
    # Create a pybids representation of the dataset
    layout = BIDSLayout(
        root=container_dataset_path,
        validate=False,
        config=resource_filename("bids_tools", "bids/config/bids.json"),
        **kwargs,
    )
    return layout


def get_subject_bidsfile_info(container_dataset_path, **kwargs):
    """Return a list of dictionaries with BIDS file information for a given subject.

    Parameters
    ----------
    container_dataset_path : str
        Path to the BIDS dataset.

    kwargs : dict
        Dictionary of arguments key/value to pass to the pybids BIDSLayout.get() function.

    Returns
    -------
    subject_info : list
        List of dictionaries with BIDS file information for a given subject.
    """
    # Create a pybids representation of the dataset
    layout = create_bids_layout(container_dataset_path)
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
            ] = extract_channels_tsv(
                file.path.split(f'_{file_info["datatype"]}')[0] + "_channels.tsv"
            )
        # Add the file information to the list
        subject_bids_file_info.append(file_info)
    # Return the list of dictionaries
    return subject_bids_file_info


def extract_channels_tsv(channels_tsv_file):
    """Extract the content from a BIDS _channels.tsv file in JSON format.

    Parameters
    ----------
    channels_tsv_file : str
        Path to the BIDS _channels.tsv file.

    Returns
    -------
    channels_json : str
        JSON representation of the content of the BIDS _channels.tsv file.
    """
    channels_df = pd.read_csv(channels_tsv_file, sep="\t")
    return channels_df.to_json(orient="records")


def get_bidsdataset_content(container_dataset_path=None):
    """Create a dictionary storing dataset information indexed by the HIP platform.

    Parameters
    ----------
    container_dataset_path : str
        Path to the BIDS dataset.

    Returns
    -------
    dataset_desc : dict
        Dictionary storing dataset information indexed by the HIP platform.
    """
    # Create a pybids representation of the dataset
    layout = create_bids_layout(container_dataset_path)
    # Load the dataset_description.json as initial dictionary-based description
    with open(
        os.path.join(container_dataset_path, "dataset_description.json"), "r"
    ) as f:
        dataset_desc = json.load(f)
    # Add basic information retrieved with pybids
    dataset_desc["DataTypes"] = layout.get_datatypes()
    dataset_desc["Formats"] = layout.get_extensions()
    dataset_desc["SessionsCount"] = len(layout.get_sessions())
    dataset_desc["Tasks"] = layout.get_tasks()
    dataset_desc["RunsCount"] = len(layout.get_runs())
    # Get general info about ieeg recordings
    seeg_info = {
        "ECOGChannelCount": 0,
        "SEEGChannelCount": 0,
        "EEGChannelCount": 0,
        "EOGChannelCount": 0,
        "ECGChannelCount": 0,
        "EMGChannelCount": 0,
        "MiscChannelCount": 0,
        "TriggerChannelCount": 0,
        "SamplingFrequency": 0,
        "RecordingDuration": 0,
    }
    for f in layout.get(suffix="ieeg"):
        f_entities_keys = f.entities.keys()
        for info_key in seeg_info:
            if info_key in f_entities_keys:
                # Keep the maximal value in case it is heterogeneous
                if f.entities[info_key] > seeg_info[info_key]:
                    seeg_info[info_key] = f.entities[info_key]
    for key, val in seeg_info.items():
        if val > 0:
            dataset_desc[key] = val
    dataset_desc["EventsFileCount"] = len(layout.get(suffix="events"))
    # Load the participants.tsv file to extract information about participants
    participants_df = pd.read_csv(
        os.path.join(container_dataset_path, "participants.tsv"),
        sep="\t",
        header=0,
        na_filter=False,
    )
    # Get min and max age of participants
    if "age" in participants_df.keys():
        dataset_desc["AgeMin"] = f'{participants_df["age"].min()}'
        dataset_desc["AgeMax"] = f'{participants_df["age"].max()}'
    else:
        dataset_desc["AgeMin"] = None
        dataset_desc["AgeMax"] = None
    dataset_desc["ParticipantsCount"] = len(participants_df.index)
    dataset_desc["ParticipantsGroups"] = (
        list(participants_df["group"].unique())
        if "group" in participants_df.keys()
        else [None]
    )
    dataset_desc["Participants"] = participants_df.to_dict(orient="records")
    del participants_df
    # Get total number of files and size
    dataset_desc["Size"] = get_dataset_size(container_dataset_path)
    dataset_desc["FileCount"] = len(layout.get_files())
    return dataset_desc


def get_dataset_size(container_dataset_path=None):
    """Return the size of the BIDS dataset in megabytes.

    Parameters
    ----------
    container_dataset_path : str
        Path to the BIDS dataset.

    Returns
    -------
    total_size_megabytes : str
        Size of the BIDS dataset in megabytes.
    """
    # Get total number of files and size
    total_size_megabytes = (
        subprocess.check_output(["du", "-sh", container_dataset_path])
        .split()[0]
        .decode("utf-8")
    )
    ## Alternative: Count only files outside sourcedata/
    # total_size_bytes = 0
    # files = layout.get_files()
    # for f in files:
    #     total_size_bytes += os.path.getsize(f)
    # # Convert once from bytes to megabytes (getsize return bytes)
    # total_size_megabytes = 1e-6 * total_size_bytes
    # total_size_megabytes = f'{total_size_megabytes:.2f}'
    # del files
    return total_size_megabytes


def get_all_datasets_content(
    input_data=None,
    output_file=None,
):
    """Return a JSON file containing a list of dataset dictionaries as response to HIP request.

    Parameters
    ----------
    input_data : str
        Path to the HIP json request.

    output_file : str
        Path to the output JSON file.
    """
    # Load the HIP json request
    with open(input_data, "r") as f:
        input_content = json.load(f)
    # Extract the list of dataset paths
    dataset_paths = [dataset["path"] for dataset in input_content["datasets"]]
    # Create a list of dictionaries storing the dataset information
    # indexed by the HIP platform
    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        datasets_desc = [
            executor.submit(get_bidsdataset_content, ds_path)
            for ds_path in dataset_paths
        ]
        datasets_desc = [f.result() for f in datasets_desc]
    # Dump the dataset_desc dict in a .json file
    if output_file:
        with open(output_file, "w") as f:
            json.dump(datasets_desc, f, indent=4)
        print(SUCCESS)
