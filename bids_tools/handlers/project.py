# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Methods supporting  the Collaborative Space of the HIP."""

import os
import shutil
import json
import pandas as pd
from pathlib import Path
from sre_constants import SUCCESS

from bids_tools.bids.dataset import create_empty_bids_dataset
from bids_tools.bids.dataset import get_bidsdataset_content


PROJECT_FOLDERS = [
    "code",
    "documents",
    "environments",
    "inputs/bids-dataset",
    "outputs",
]
DOCUMENTS_FOLDERS = ["clinical", "reports", "protocols", "other"]


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

    # Create initial documents directory structure
    for folder in DOCUMENTS_FOLDERS:
        os.makedirs(project_dir / "documents" / folder, exist_ok=True)

    # Create initial project README.md file
    with open(project_dir / "README.md", "w") as f:
        f.writelines([f"# {project_title}\n\n", f"{project_description}"])


def create_project(input_data: str, output_file: str):
    """Create a new Collaborative Project on the HIP initialized with directory/file structure.

    Parameters
    ----------
    input_data : str
        Path to input data JSON file sent by the HIP that contains all information
        about Project and corresponding BIDS dataset in the form::

            {
                "path": "/path/to/project/directory",
                "title": "Project Title",
                "description": "Project Description that would be put in the README.md file",
                "datasetDescription": {
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

    output_file : str
        Path to output file that will contain the JSON summary of the BIDS dataset of the project.
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)
    print(f'Creating new collaborative project at {input_data["path"]}...')
    # Extract input data
    project_dir = Path(input_data["path"])
    project_title = input_data["title"]
    project_description = input_data["description"]
    # Initialize project directory structure with README.md file
    initialize_project_structure(project_dir, project_title, project_description)
    # Create initial BIDS dataset
    create_empty_bids_dataset(
        bids_dir=(project_dir / "inputs" / "bids-dataset").absolute(),
        dataset_desc=input_data["datasetDescription"],
    )
    # Create output file with summary of BIDS dataset
    dataset_content = get_bidsdataset_content(
        bids_dir=str((project_dir / "inputs" / "bids-dataset").absolute()),
    )
    with open(output_file, "w") as f:
        json.dump(dataset_content, f, indent=4)
    print(SUCCESS)


def import_subject(input_data: str, output_file: str):
    """Import a new subject from a BIDS dataset of the HIP Center space to the BIDS dataset of the HIP Collaborative Project.

    Parameters
    ----------
    input_data : str
        Path to input data JSON file sent by the HIP that contains all information
        about the subject and files to import in the form::

            {
                "sourceDatasetPath": "/path/to/source/bids/dataset/directory",
                "participantId": "sub-01",
                "targetDatasetPath": "/path/to/target/bids/dataset/directory",
            }

    output_file : str
        Path to output file that will contain the JSON summary of the BIDS dataset of the project.
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)
    print(
        f"Importing subject {input_data['participantId']} "
        f"from {input_data['sourceDatasetPath']} "
        f"to {input_data['targetDatasetPath']}..."
    )
    # Copy subject directory from source to target
    shutil.copytree(
        (
            Path(input_data["sourceDatasetPath"]) / input_data["participantId"]
        ).absolute(),
        (
            Path(input_data["targetDatasetPath"]) / input_data["participantId"]
        ).absolute(),
        dirs_exist_ok=True,
    )
    # Update participants.tsv file of target dataset with subject row from source dataset
    transfer_subject_participants_tsv_row(
        participant_id=input_data["participantId"],
        source_participant_tsv=(
            Path(input_data["sourceDatasetPath"]) / "participants.tsv"
        ).absolute(),
        target_participants_tsv=(
            Path(input_data["targetDatasetPath"]) / "participants.tsv"
        ).absolute(),
    )
    # Create output file with summary of BIDS dataset
    dataset_content = get_bidsdataset_content(
        bids_dir=str((Path(input_data["targetDatasetPath"])).absolute()),
    )
    with open(output_file, "w") as f:
        json.dump(dataset_content, f, indent=4)
    print(SUCCESS)


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


def import_document(input_data: str):
    """Import a new supporting document to the `documents/` folder of the HIP Collaborative Project.

    Parameters
    ----------
    input_data : str
        Path to input data JSON file sent by the HIP that contains all information
        about the document to import in the form::

            {
                "sourceDocumentAbsPath": "/path/to/source/document/file",
                "targetProjectAbsPath": "/path/to/target/project/directory",
                "sourceDocumentRelPath": "/project/relative/path/to/target/document/file",
            }
    """
    # Load input data
    with open(input_data, "r") as f:
        input_data = json.load(f)
    # Extract input data
    source_document_path = Path(input_data["sourceDocumentAbsPath"])
    target_document_path = (
        Path(input_data["targetProjectAbsPath"]) / input_data["targetDocumentRelPath"]
    )
    # Print information
    print(
        f"Importing document {source_document_path} from HIP Center space "
        f"to HIP Collaborative Project at {target_document_path}... "
    )
    # Create intermediate directories if they don't exist
    os.makedirs(target_document_path.parent, exist_ok=True)
    # Remove target document if it already exists
    if target_document_path.exists():
        print(f"WARNING: Overwriting target document at {target_document_path}...")
        os.remove(target_document_path)
    # Copy document from source to target
    shutil.copyfile(source_document_path, target_document_path)
    print(SUCCESS)
