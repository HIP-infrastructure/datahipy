# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Test the datahipy CLI "sub.*" commands."""

from __future__ import absolute_import
import os
import pytest
import json
import datalad
from datalad.support.gitrepo import GitRepo


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset.py::test_run_dataset_create_init_tag")
def test_run_sub_import(script_runner, input_path, dataset_path, io_path):
    # Create input data
    input_data = {
        "subjects": [{"sub": "carole", "age": "25", "sex": "M", "hospital": "CHUV"}],
        "files": [
            {
                "modality": "ieeg",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/SZ1.TRC",
                "entities": {
                    "sub": "carole",
                    "ses": "postimp",
                    "task": "stimulation",
                    "acq": "1024hz",
                },
            },
            {
                "modality": "ieeg",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/SZ2.TRC",
                "entities": {
                    "sub": "carole",
                    "ses": "postimp",
                    "task": "stimulation",
                    "acq": "1024hz",
                },
            },
            {
                "modality": "T1w",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/3DT1post_deface.nii",
                "entities": {
                    "sub": "carole",
                    "ses": "postimp",
                    "acq": "lowres",
                    "ce": "gadolinium",
                },
            },
            {
                "modality": "T1w",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/3DT1post_deface_2.nii",
                "entities": {
                    "sub": "carole",
                    "ses": "postimp",
                    "acq": "lowres",
                    "ce": "gadolinium",
                },
            },
            {
                "modality": "T1w",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/3DT1pre_deface.nii",
                "entities": {
                    "sub": "carole",
                    "ses": "preimp",
                    "acq": "lowres",
                },
            },
            {
                "modality": "ct",
                "subject": "carole",
                "path": f"{input_path}/sub-carole/3DCTpost_deface.nii",
                "entities": {
                    "sub": "carole",
                    "ses": "postimp",
                    "acq": "electrodes",
                },
            },
        ],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "import_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy sub.import command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.import",
        "--input_data",
        input_file,
        "--dataset_path",
        dataset_path,
        "--input_path",
        input_path,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the sub-carole folder was created
    assert os.path.exists(os.path.join(dataset_path, "sub-carole"))


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset.py::test_run_datasets_get")
def test_run_sub_get(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"owner": "hipadmin", "path": dataset_path, "sub": "carole"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "get_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "get_sub_output.json")
    # Run datahipy sub.get command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.get",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
        "--dataset_path",
        dataset_path,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the output file was created
    assert os.path.exists(output_file)


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub_get")
def test_run_sub_edit_clinical(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "subject": "carole",
        "clinical": {
            "age": "30",
            "sex": "M",
            "handedness": "L",
            "hospital": "CHUGA",
        },
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "sub_edit_clinical.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output updated participants.tsv file
    output_file = os.path.join(dataset_path, "participants.tsv")
    # Run datahipy sub.edit.clinical command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.edit.clinical",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
        "--dataset_path",
        dataset_path,
    )
    # Check that the command ran successfully
    assert ret.success


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project.py::test_run_project_get_tags")
def test_run_project_sub_delete(script_runner, project_path, io_path):
    # Create input data
    input_data = {"subject": "carole"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "delete_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy sub.delete command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.delete",
        "--input_data",
        input_file,
        "--dataset_path",
        os.path.join(project_path, "inputs", "bids-dataset"),
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the sub-carole folder was deleted
    assert not os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", "sub-carole")
    )


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(
    after="test_run_project_sub_delete"
)  # delete sub-carole only after project tests are done
def test_run_sub_delete_file(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "files": [
            {
                "subject": "carole",
                "modality": "Anat",
                "fullpath": "sub-carole/ses-postimp/anat/sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-2_T1w.nii",
            }
        ]
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "delete_sub_file.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy sub.delete.file command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.delete.file",
        "--input_data",
        input_file,
        "--dataset_path",
        dataset_path,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the file was deleted
    assert not os.path.exists(
        os.path.join(
            dataset_path,
            os.path.join(
                "sub-carole",
                "ses-postimp",
                "anat",
                "sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-2_T1w.nii",
            ),
        )
    )


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub_delete_file")
def test_run_sub_delete(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"subject": "carole"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "delete_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy sub.delete command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "sub.delete",
        "--input_data",
        input_file,
        "--dataset_path",
        dataset_path,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the sub-carole folder was deleted
    assert not os.path.exists(os.path.join(dataset_path, "sub-carole"))
