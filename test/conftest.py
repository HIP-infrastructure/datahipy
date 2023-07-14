# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Define fixtures for testing datahipy package."""

import os
import pytest
import shutil


@pytest.fixture(scope="session", autouse=True)
def dataset_name():
    return "NEW_BIDS_DS"


@pytest.fixture(scope="session", autouse=True)
def project_name():
    return "NEW_PROJECT"


@pytest.fixture(scope="session", autouse=True)
def dataset_path(dataset_name):
    dataset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tmp", dataset_name)
    )
    if os.path.exists(dataset_path):
        git_dir = os.path.join(dataset_path, ".git")
        if os.path.exists(git_dir):
            os.system(f"chmod -R a+w {git_dir}")
        shutil.rmtree(dataset_path)
    return dataset_path


@pytest.fixture(scope="session", autouse=True)
def io_path():
    io_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp", "io"))
    if os.path.exists(io_path):
        shutil.rmtree(io_path)
    os.makedirs(io_path, exist_ok=True)
    return io_path


@pytest.fixture(scope="session", autouse=True)
def input_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))


@pytest.fixture(scope="session", autouse=True)
def project_path(project_name):
    project_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tmp", project_name)
    )
    if os.path.exists(project_path):
        git_dir = os.path.join(project_path, ".git")
        if os.path.exists(git_dir):
            os.system(f"chmod -R a+w {git_dir}")
        bids_git_dir = os.path.join(project_path, "inputs", "bids-dataset", ".git")
        if os.path.exists(bids_git_dir):
            os.system(f"chmod -R a+w {bids_git_dir}")
        shutil.rmtree(project_path)
    return project_path
