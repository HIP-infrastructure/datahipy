# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Test the datahipy CLI "project.*" commands."""

from __future__ import absolute_import
import os
import pytest
import json
import datalad
from datalad.support.gitrepo import GitRepo


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub.py::test_run_sub_edit_clinical")
def test_run_project_create(script_runner, project_path, io_path):
    # Create input data
    input_data = {
        "path": project_path,
        "title": "New Project Title",
        "description": "Project Description that would be put in the README.md file",
        "datasetDescription": {
            "Name": "BIDS Dataset Title",
            "BIDSVersion": "1.6.0",
            "License": "CC-BY-4.0",
            "Authors": ["Author 1", "Author 2"],
            "Acknowledgements": "Acknowledgement 1",
            "Funding": ["Funding 1"],
            "ReferencesAndLinks": ["Reference 1", "Reference 2"],
            "DatasetDOI": "",
        },
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "create_project.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "create_project_output.json")
    # Run datahipy project.create command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "project.create",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success
    assert os.path.exists(output_file)
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "README.md"))
    assert os.path.exists(os.path.join(project_path, "inputs"))
    assert os.path.exists(os.path.join(project_path, "outputs"))
    assert os.path.exists(os.path.join(project_path, "code"))
    assert os.path.exists(os.path.join(project_path, "environments"))
    assert os.path.exists(os.path.join(project_path, "inputs", "bids-dataset"))
    assert os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", "dataset_description.json")
    )
    assert os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", "participants.tsv")
    )
    assert os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", "CHANGES")
    )
    assert os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", "README")
    )
    assert os.path.exists(
        os.path.join(project_path, "inputs", "bids-dataset", ".bidsignore")
    )


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project_create")
def test_run_project_create_init_tag(script_runner, project_path, io_path):
    # Create input data
    input_data = {
        "path": project_path,
        "tag": "0.0.0",
        "message": "- Initial project",
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "project_create_init_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.create_tag command
    ret = script_runner.run(
        "datahipy", "--command", "project.create_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the tag was created
    assert "0.0.0" in [
        tag_dict["name"] for tag_dict in GitRepo(project_path).get_tags()
    ]


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project_create_init_tag")
def test_run_project_sub_import(script_runner, dataset_path, project_path, io_path):
    # Create input data
    input_data = {
        "sourceDatasetPath": dataset_path,
        "participantId": "sub-carole",
        "targetDatasetPath": os.path.join(project_path, "inputs", "bids-dataset"),
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "import_project_sub.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "import_project_sub_output.json")
    # Run datahipy project.sub.import command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "project.sub.import",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success
    assert os.path.exists(output_file)
    assert os.path.exists(
        os.path.join(
            project_path,
            "inputs",
            "bids-dataset",
            "sub-carole",
            "ses-postimp",
            "anat",
            "sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-2_T1w.nii",
        )
    )


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project_sub_import")
def test_run_project_doc_import(script_runner, dataset_path, project_path, io_path):
    # Create input data
    input_data = {
        "sourceDocumentAbsPath": os.path.join(dataset_path, "participants.tsv"),
        "targetProjectAbsPath": project_path,
        "targetDocumentRelPath": os.path.join("documents", "other", "participants.tsv"),
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "import_project_doc.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy project.doc.import command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "project.doc.import",
        "--input_data",
        input_file,
    )
    # Check that the command ran successfully
    assert ret.success
    assert os.path.exists(
        os.path.join(project_path, "documents", "other", "participants.tsv")
    )


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project_doc_import")
def test_run_project_create_tag(script_runner, project_path, io_path):
    # Create input data
    input_data = {
        "path": project_path,
        "tag": "1.0.0",
        "message": "- Import sub-carole data from existing dataset",
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "project_create_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.create_tag command
    ret = script_runner.run(
        "datahipy", "--command", "project.create_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the tag was created
    assert "1.0.0" in [
        tag_dict["name"] for tag_dict in GitRepo(project_path).get_tags()
    ]


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_project_create_tag")
def test_run_project_get_tags(script_runner, project_path, io_path):
    # Create input data
    input_data = {
        "path": project_path,
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "project_get_tags.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "project_get_tags_output.json")
    # Run datahipy dataset.get_tags command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "project.get_tags",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the output file was created
    assert os.path.exists(output_file)
    # Load the output json file and check the tag
    with open(output_file, "r") as f:
        output_data = json.load(f)
    assert "1.0.0" in output_data["tags"]
    assert output_data["path"] == project_path


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub.py::test_run_project_sub_delete")
def test_run_project_checkout_tag(script_runner, project_path, io_path):
    # Create input data
    input_data = {"path": project_path, "tag": "0.0.0"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "project_checkout_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.checkout.tag command
    ret = script_runner.run(
        "datahipy", "--command", "project.checkout_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
