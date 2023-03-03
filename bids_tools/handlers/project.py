# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Methods supporting  the Collaborative Space of the HIP."""

import os
import shutil
import json
import pandas as pd
from pathlib import Path

from bids_tools.bids.dataset import create_empty_bids_dataset


PROJECT_FOLDERS = ["code", "documents", "inputs/bids-dataset", "outputs"]

PROJECT_DOCUMENTS = [
    "README.md",
]


def initialize_project_structure(
    project_dir: Path, project_title: str, project_description: str
):
    """Initialize the directory structure of a Collaborative Project on the HIP.

    Parameters
    ----------
    project_dir : pathlib.Path
        Path to the project directory.

    project_title : str
        Title of the project.

    project_description : str
        Description of the project.
    """
    # Create initial project directory structure
    for folder in PROJECT_FOLDERS:
        os.makedirs(project_dir / folder, exist_ok=True)

    # Create initial project README.md file
    with open(project_dir / "README.md", "w") as f:
        f.writelines([f"# {project_title}\n\n", f"{project_description}"])


def create_project(input_data: dict):
    """Create a new Collaborative Project on the HIP initialized with directory/file structure.

    Parameters
    ----------
    input_data : dict
        Dictionary sent by the HIP that contains all information
        about Project and corresponding BIDS dataset in the form::

            {
                "path": "/path/to/project/directory",
                "title": "Project Title",
                "description": "Project Description that would be put in the README.md file",
                "createBidsDatasetDto": {
                    "owner": "username",
                    "parent_path": "/path/to/project/directory/inputs",
                    "dataset_dirname": "bids-dataset",
                    "DatasetDescJSON": {
                        "Name": "BIDS Dataset Title",
                        "BIDSVersion": "1.6.0",
                        "License": "CC-BY-4.0",
                        "Authors": ["Author 1", "Author 2"],
                        "Acknowledgements": "Acknowledgement 1",
                        "Funding": ["Funding 1"],
                        "ReferencesAndLinks": ["Reference 1", "Reference 2"],
                        "DatasetDOI": "10.18112/openneuro.ds000000.v1.0.0"
                    }
                }
            }
    """
    # Extract input data
    project_dir = Path(input_data["path"])
    project_title = input_data["title"]
    project_description = input_data["description"]
    # Initialize project directory structure with README.md file
    initialize_project_structure(project_dir, project_title, project_description)
    # Create initial BIDS dataset
    create_empty_bids_dataset(
        bids_dir=(project_dir / "inputs" / "bids-dataset").absolute(),
        dataset_desc=input_data["createBidsDatasetDto"],
    )


def import_subject(input_data: dict):
    """Import a new subject from a BIDS dataset of the HIP Center space to the BIDS dataset of the HIP Collaborative Project.

    Parameters
    ----------
    input_data : dict
        Dictionary sent by the HIP that contains all information
        about the subject and files to import in the form::

            {
                "sourceDatasetPath": "/path/to/source/bids/dataset/directory",
                "subject": "sub-01",
                "targetDatasetPath": "/path/to/target/bids/dataset/directory",
            }
    """
    # Copy subject directory from source to target
    shutil.copytree(
        Path(input_data["sourceDatasetPath"] / input_data["subject"]).absolute(),
        Path(input_data["targetDatasetPath"] / input_data["subject"]).absolute(),
    )
    # Update participants.tsv file of target dataset with subject row from source dataset
    transfer_subject_participants_tsv_row(
        participant_id=input_data["subject"],
        source_participant_tsv=Path(
            input_data["sourceDatasetPath"] / "participants.tsv"
        ).absolute(),
        target_participants_tsv=Path(
            input_data["targetDatasetPath"] / "participants.tsv"
        ).absolute(),
    )


def transfer_subject_participants_tsv_row(
    participant_id: str, source_participant_tsv: str, target_participants_tsv: str
):
    """Transfer subject row from the participants.tsv file of the source to the participants.tsv file of the target BIDS dataset.

    Parameters
    ----------
    participant_id : str
        ID of the participant to transfer (e.g. "sub-01").

    source_participant_tsv : str
        Path to the participants.tsv file of the source BIDS dataset.

    target_participants_tsv : str
        Path to the participants.tsv file of the target BIDS dataset.
    """
    # Extract subject line from participants.tsv file of source dataset as dataframe
    source_participants_df = pd.read_csv(source_participant_tsv, sep="\t")
    source_subject_df = source_participants_df[
        source_participants_df["participant_id"] == participant_id
    ]
    # Extract participants.tsv file of target dataset as dataframe
    target_participants_df = pd.read_csv(target_participants_tsv, sep="\t")
    # Append subject row dataframe to target dataframe
    target_participants_df = pd.concat(
        [target_participants_df, source_subject_df], join="outer"
    )
    # Replace any NaN values with 'n/a' following BIDS convention
    target_participants_df = target_participants_df.fillna("n/a")
    # Write updated participants.tsv file of target dataset
    target_participants_df.to_csv(target_participants_tsv, sep="\t", index=False)


def import_document(input_data: dict):
    """Import a new supporting document to the `documents/` folder of the HIP Collaborative Project.

    Parameters
    ----------
    input_data : dict
        Dictionary sent by the HIP that contains all information
        about the document to import in the form::

            {
                "sourceDocumentPath": "/path/to/source/document/file",
                "targetDocumentPath": "/path/to/target/document/file",
            }
    """
    source_document_path = Path(input_data["sourceDocumentPath"])
    target_document_path = Path(input_data["targetDocumentPath"])
    # Copy document from source to target
    shutil.copyfile(source_document_path, target_document_path)
