# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Functions for validating BIDS datasets."""

import json
import subprocess


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
