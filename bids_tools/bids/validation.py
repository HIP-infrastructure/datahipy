# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Functions for validating BIDS datasets."""

import json
import subprocess
from os import path as op
from bids_tools.bids.const import BIDS_VERSION


def validate_bids_dataset(container_dataset_path, *args):
    """Validate a BIDS dataset using the BIDS Validator.

    Parameters
    ----------
    container_dataset_path : str
        Path to the BIDS dataset

    args : list
        List of options to pass to the `bids-validator`.
        Can be used to ignore warnings (`["--ignoreWarnings"]`)
        or nifti headers (`["--ignoreNiftiHeaders"]`) or to
        skip checking that any given file for one subject
        is present for all other subjects (`["--ignoreSubjectConsistency"]`)
        or to use a specific BIDS schema (`["-s", "v1.6.0"]`)

    Returns
    -------
    output : dict
        Output of the bids-validator as a dictionary.

    return_code : int
        Return code of the bids-validator.
    """
    # Create the bids-validator command to run
    command = ["bids-validator", container_dataset_path] + list(args)
    # Add the --json option if not already present
    if "--json" not in list(args):
        command.append("--json")
    # Run the command to validate the dataset
    print(f'Execute cmd: {" ".join(command)}')
    output = subprocess.run(command, capture_output=True)
    print(f"Output: {output}")
    # Return the JSON string output as a dictionary and the return code
    return json.loads(output.stdout.decode()), output.returncode


def add_bidsignore_validation_rule(bids_dir, rule):
    """Create/update a `.bidsignore` file to ignore specific files by the BIDS Validator.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    rule : str
        Rule to add to the `.bidsignore` file,
        e.g. "**/*_ct.*" to ignore all CT files.
    """
    bidsignore_path = op.join(bids_dir, ".bidsignore")
    if not op.exists(bidsignore_path):
        with open(bidsignore_path, "w") as f:
            f.write(f"{rule}\n")
    else:
        with open(bidsignore_path, "r") as f:
            bidsignore_content = f.read()
        if f"{rule}" not in bidsignore_content:
            with open(bidsignore_path, "a") as f:
                f.write(f"{rule}\n")


def get_bids_validator_output_info(bids_dir, bids_schema_version=None):
    """Run the bids-validator on the dataset with the specified schema version and the option to ignore subject consistency.

    Parameters
    ----------
    bids_dir : str
        Path to the BIDS dataset.

    bids_schema_version : str
        BIDS schema version to use for the validation.
        (e.g. "v1.7.0")

    Returns
    -------
    bids_validator_output_info : dict
        Dictionary containing the bids-validator output
        to be integrated in the dataset content to be indexed.
    """
    # If no bids_schema_version is specified, use the default BIDS_VERSION
    if not bids_schema_version:
        bids_schema_version = BIDS_VERSION
    # Initialize the dictionary to store the bids-validator output
    bids_validator_output_info = {}
    # Run the bids-validator on the dataset with the specified schema version and
    # the option to ignore subject consistency
    validator_opts = [
        "--ignoreWarnings",
        "--ignoreSubjectConsistency",
        "-s",
        bids_schema_version,
    ]
    validator_output, validator_returncode = validate_bids_dataset(
        bids_dir, *validator_opts
    )
    # Extract validator output to the bids_validator_output_info dictionary
    bids_validator_output_info["BIDSSchemaVersion"] = bids_schema_version
    bids_validator_output_info["BIDSErrors"] = validator_output["issues"][
        "errors"
    ]
    bids_validator_output_info["BIDSWarnings"] = validator_output["issues"][
        "warnings"
    ]
    bids_validator_output_info["BIDSIgnored"] = validator_output["issues"][
        "ignored"
    ]
    bids_validator_output_info["BIDSValid"] = validator_returncode == 0
    # Return the bids-validator output dictionary to be integrated
    # in the dataset content to be indexed
    return bids_validator_output_info
