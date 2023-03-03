# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Methods supporting  the Collaborative Space of the HIP."""


def create_project(input_data):
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
                "bids_dataset": {
                    "path": "/path/to/bids/dataset/directory",
                    "title": "BIDS Dataset Title",
                    "description": "BIDS Dataset Description that would be put in the README.md file",
                    "authors": ["Author 1", "Author 2"],
                    "license": "CC-BY-4.0"
                }

            }

    """


def import_subject(input_data):
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


def import_document(input_data):
    """Import a new supporting document supporting to the `documents/` folder of the HIP Collaborative Project.

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
