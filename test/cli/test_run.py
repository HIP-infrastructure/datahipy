from __future__ import absolute_import
import os
import pytest
import json


@pytest.mark.script_launch_mode("subprocess")
def test_run_help(script_runner):
    ret = script_runner.run("bids_tools", "-h")
    assert ret.success


@pytest.mark.script_launch_mode("subprocess")
def test_run_dataset_create(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "dataset_dirname": "NEW_BIDS_DS",
        "DatasetDescJSON": {
            "Name": "My New BIDS dataset",
            "BIDSVersion": "1.4.0",
            "License": "n/a",
            "Authors": ["Tom", "Jerry"],
            "Acknowledgements": "Overwrite test",
            "HowToAcknowledge": "n/a",
            "Funding": "Picsou",
            "ReferencesAndLinks": "n/a",
            "DatasetDOI": "n/a",
        },
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "create_dataset.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run bids_tools dataset.create command
    ret = script_runner.run(
        "bids_tools",
        "--command",
        "dataset.create",
        "--input_data",
        input_file,
        "--dataset_path",
        os.path.dirname(dataset_path),
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the dataset was created by checking for the dataset_description.json file
    assert os.path.exists(os.path.join(dataset_path, "dataset_description.json"))


@pytest.mark.script_launch_mode("subprocess")
def test_run_sub_import(script_runner, input_path, dataset_path, io_path):
    # Create input data
    input_data = {
        "subjects": [{"sub": "carole", "age": "25", "sex": "M", "hospital": "CHUV"}],
        "files": [
            {
                "modality": "ieeg",
                "subject": "carole",
                "path": "sub-carole/SZ1.TRC",
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
                "path": "sub-carole/SZ2.TRC",
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
                "path": "sub-carole/3DT1post_deface.nii",
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
                "path": "sub-carole/3DT1post_deface_2.nii",
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
                "path": "sub-carole/3DT1pre_deface.nii",
                "entities": {"sub": "carole", "ses": "preimp", "acq": "lowres"},
            },
        ],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "import_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run bids_tools sub.import command
    ret = script_runner.run(
        "bids_tools",
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
def test_run_dataset_get(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"owner": "hipadmin", "path": dataset_path}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "get_dataset.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "get_dataset_output.json")
    # Run bids_tools dataset.get command
    ret = script_runner.run(
        "bids_tools",
        "--command",
        "dataset.get",
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
def test_run_datasets_get(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "owner": "hipadmin",
        "datasets": [{"path": dataset_path}, {"path": dataset_path}],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "get_datasets.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "get_datasets_output.json")
    # Run bids_tools datasets.get command
    ret = script_runner.run(
        "bids_tools",
        "--command",
        "datasets.get",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success


@pytest.mark.script_launch_mode("subprocess")
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
    # Run bids_tools sub.get command
    ret = script_runner.run(
        "bids_tools",
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
def test_run_sub_edit_clinical(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "subject": "carole",
        "clinical": {"age": "30", "sex": "M", "handedness": "L", "hospital": "CHUGA"},
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "sub_edit_clinical.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output updated participants.tsv file
    output_file = os.path.join(dataset_path, "participants.tsv")
    # Run bids_tools sub.edit.clinical command
    ret = script_runner.run(
        "bids_tools",
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
def test_run_sub_delete_file(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "files": [
            {
                "subject": "carole",
                "modality": "Anat",
                "fullpath": "sub-carole/ses-postimp/anat/sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-02_T1w.nii",
            }
        ]
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "delete_sub_file.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run bids_tools sub.delete.file command
    ret = script_runner.run(
        "bids_tools",
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
                "sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-02_T1w.nii",
            ),
        )
    )


@pytest.mark.script_launch_mode("subprocess")
def test_run_sub_delete(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"subject": "carole"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "delete_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run bids_tools sub.delete command
    ret = script_runner.run(
        "bids_tools",
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
