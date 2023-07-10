# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to retrieve BIDS dataset content to be indexed by the Elasticsearch engine of the HIP."""

import os
import json
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pkg_resources import resource_filename
from sre_constants import SUCCESS
from datetime import date

from bids import BIDSLayout

import datalad.api

from datahipy.bids.electrophy import get_ieeg_info
from datahipy.bids.participant import get_participants_info
from datahipy.bids.validation import (
    add_bidsignore_validation_rule,
    get_bids_validator_output_info,
)
from datahipy.bids.version import determine_bids_schema_version


# Set the number of threads to use for parallel processing
# Modify this value if you want to use more or less threads or
# if you want to set it to 1 to avoid parallel processing
NUM_THREADS = os.cpu_count() - 1 if os.cpu_count() > 1 else 1


def create_initial_bids_readme(bids_dir, dataset_desc):
    """Create an initial `README` file for a BIDS dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    dataset_desc : dict
        Dictionary with the content of the dataset_description.json file.
    """
    with open(os.path.join(bids_dir, "README"), "w") as f:
        f.writelines(
            [
                f'# {dataset_desc["Name"]}\n\n',
                f"To be completed...\n\n",
                f"Use it as the dataset landing page, "
                "which should provide enough information "
                "about the dataset and its creation context.",
            ]
        )


def create_initial_bids_changes(bids_dir):
    """Create an initial `CHANGES` file for a BIDS dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.
    """
    with open(os.path.join(bids_dir, "CHANGES"), "w") as f:
        f.writelines(
            [
                f"0.0.0 {date.today().strftime('%Y-%m-%d')}\n",
                "\t- Creation of the dataset.",
            ]
        )


def create_initial_participants_tsv(bids_dir):
    """Create an initial `participants.tsv` file for a BIDS dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.
    """
    with open(os.path.join(bids_dir, "participants.tsv"), "w") as f:
        f.write("participant_id\tage\tsex\tgroup")


def create_empty_bids_dataset(bids_dir=None, dataset_desc=None):
    """Create an empty BIDS dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    dataset_desc : dict
        Dictionary with the content of the dataset_description.json file.
    """
    print("> Creating an empty BIDS dataset at: ", bids_dir, "...")
    # Create the BIDS dataset directory if it does not exist
    if not os.path.exists(os.path.dirname(bids_dir)):
        os.makedirs(bids_dir, exist_ok=True)
    # Initialize the BIDS dataset as a Datalad-managed dataset
    datalad.api.create(
        dataset=bids_dir,
        cfg_proc=['text2git', 'bids']
    )
    # Create the dataset_description.json file
    with open(os.path.join(bids_dir, "dataset_description.json"), "w") as f:
        json.dump(dataset_desc, f, indent=4)
    # Create initial README file
    create_initial_bids_readme(bids_dir, dataset_desc)
    # Create initial CHANGES file
    create_initial_bids_changes(bids_dir)
    # Create the .bidsignore file and add the line to ignore CT files
    # (not yet supported by the validator)
    add_bidsignore_validation_rule(bids_dir, "**/*_ct.*")
    # Create an initial participants.tsv file
    create_initial_participants_tsv(bids_dir)
    # Save the state of the initial dataset
    datalad.api.save(
        dataset=bids_dir,
        message='Initial blank BIDS dataset',
        recursive=True
    )


def create_bids_layout(bids_dir=None, **kwargs):
    """Create a pybids representation of a BIDS dataset.

    Parameters
    ----------
    bids_dir : str
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
        root=bids_dir,
        validate=False,
        config=resource_filename("datahipy", "bids/config/bids.json"),
        **kwargs,
    )
    return layout


def get_bids_layout_info(bids_dir):
    """Return a dictionary with information retrieved via the PyBIDS BIDSLayout object representation of the dataset.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    Returns
    -------
    bids_layout_info : dict
        Dictionary with information retrieved via the PyBIDS BIDSLayout object representation of the dataset.
    """
    # Initialize the dictionary to be returned
    bids_layout_info = {}
    # Create a pybids representation of the dataset
    layout = create_bids_layout(bids_dir)
    # Add basic information retrieved with pybids to dataset_desc
    bids_layout_info["DataTypes"] = layout.get_datatypes()
    bids_layout_info["Formats"] = layout.get_extensions()
    bids_layout_info["SessionsCount"] = len(layout.get_sessions())
    bids_layout_info["Tasks"] = layout.get_tasks()
    bids_layout_info["RunsCount"] = len(layout.get_runs())
    # Get general info about ieeg recordings
    if "ieeg" in bids_layout_info["DataTypes"]:
        bids_layout_info.update(get_ieeg_info(layout))
    # Get the number of events files
    bids_layout_info["EventsFileCount"] = len(layout.get(suffix="events"))
    # Get the number of files
    bids_layout_info["FileCount"] = len(layout.get_files())
    return bids_layout_info


def get_dataset_size(bids_dir=None):
    """Return the size of the BIDS dataset in megabytes.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    Returns
    -------
    total_size_megabytes : str
        Size of the BIDS dataset in megabytes.
    """
    # Get total number of files and size
    total_size_megabytes = (
        subprocess.check_output(["du", "-sh", bids_dir]).split()[0].decode("utf-8")
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


def get_bidsdataset_content(bids_dir=None):
    """Create a dictionary storing dataset information indexed by the HIP platform.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    Returns
    -------
    dataset_desc : dict
        Dictionary storing dataset information indexed by the HIP platform.
    """
    # Load the dataset_description.json as initial dictionary-based description
    with open(os.path.join(bids_dir, "dataset_description.json"), "r") as f:
        dataset_desc = json.load(f)
    # Load the participants.tsv file to extract information about participants
    dataset_desc.update(get_participants_info(bids_dir=bids_dir))
    # Get the dataset size
    dataset_desc["Size"] = get_dataset_size(bids_dir)
    # Check if the field BIDSVersion is present in the dataset_description.json.
    # If not, use the default BIDS_VERSION. If present, add 'v' to match the
    # schema version expected by the validator
    bids_schema_version = determine_bids_schema_version(dataset_desc)
    # Create the .bidsignore file if it does not exist and
    # add the line to ignore CT files (not yet supported by the validator)
    add_bidsignore_validation_rule(bids_dir, "**/*_ct.*")
    # Run the bids-validator on the dataset with the specified schema version and
    # update dataset_desc with the execution dictionary output
    dataset_desc.update(get_bids_validator_output_info(bids_dir, bids_schema_version))
    # Add information retrieved with pybids to dataset_desc
    dataset_desc.update(get_bids_layout_info(bids_dir))
    # Return the created dataset_desc dictionary to be indexed
    return dataset_desc


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
