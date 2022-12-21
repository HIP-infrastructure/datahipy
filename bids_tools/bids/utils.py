# Copyright (C) 2022, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.
"""Utility function using pybids."""

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import asyncio
import nest_asyncio

import json
import pandas as pd
from sre_constants import SUCCESS
from bids import BIDSLayout

nest_asyncio.apply()

NUM_THREADS = os.cpu_count() - 1 if os.cpu_count() > 1 else 1

'''
def get_subject_info(
    container_dataset_path=None,
    subject_id=None,
    session_id=None,
    task_id=None,
    run_id=None,
):
    """Return a dictionary with the subject information."""
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

    # Get the list of files for the given subject (and session, task and run if provided)
    files = layout.get(
        subject=subject_id,
        session=session_id,
        task=task_id,
        run=run_id
    )

    for file in files:
        modality = file.entities["suffix"]
        del file.entities["suffix"]
        del file.entities["extension"]
        del file.entities["datatype"]


    bidsfile_list = []

    # Get the subject information
    subject_info = {}
    subject_info["subject_id"] = subject_id
    subject_info["session_id"] = session_id
    subject_info["task_id"] = task_id
    subject_info["run_id"] = run_id
    subject_info["subject_age"] = None
    subject_info["subject
'''


def get_bidsdataset_content(container_dataset_path=None):
    """Create a dictionary storing dataset information indexed by the HIP platform."""
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

    print(f'Extract file {os.path.join(container_dataset_path, "participants.tsv")}')
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
    total_size_megabytes = (
        subprocess.check_output(["du", "-sh", container_dataset_path])
        .split()[0]
        .decode("utf-8")
    )
    dataset_desc["Size"] = total_size_megabytes
    dataset_desc["FileCount"] = len(layout.get_files())
    ## Alternative: Count only files outside sourcedata/
    # total_size_bytes = 0
    # files = layout.get_files()
    # for f in files:
    #     total_size_bytes += os.path.getsize(f)
    # # Convert once from bytes to megabytes (getsize return bytes)
    # total_size_megabytes = 1e-6 * total_size_bytes
    # total_size_megabytes = f'{total_size_megabytes:.2f}'
    # del files

    return dataset_desc


def get_all_datasets_content(
    input_data=None,
    output_file=None,
):
    """Return a JSON file containing a list of dataset dictionaries as response to HIP request."""
    # Load the HIP json request
    with open(input_data, "r") as f:
        input_content = json.load(f)

    # Extract the list of dataset paths
    dataset_paths = [dataset["path"] for dataset in input_content["datasets"]]

    # Create a list of dictionaries storing the dataset information
    # indexed by the HIP platform
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Run asyncio tasks in a limited thread pool.
        # It should be equivalent to the following sequential code:
        # datasets_desc = [
        #     get_bidsdataset_content(
        #         container_dataset_path=ds_path,
        #     )
        #     for ds_path in dataset_paths
        #     # for ds_path, ds_name in zip(dataset_paths, dataset_names)
        # ]
        loop = asyncio.new_event_loop()

        get_bidsdataset_content_tasks = [
            loop.run_in_executor(executor, get_bidsdataset_content, ds_path)
            for ds_path in dataset_paths
        ]

        try:
            datasets_desc = loop.run_until_complete(
                asyncio.gather(*get_bidsdataset_content_tasks)
            )
        finally:
            loop.close()

    # Dump the dataset_desc dict in a .json file
    if output_file:
        with open(output_file, "w") as f:
            json.dump(datasets_desc, f, indent=4)
        print(SUCCESS)
