# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Define fixtures for testing datahipy package."""

import os
import pytest
import shutil


def fix_permissions(path):
    """Fix permissions of a path."""
    if os.path.exists(path):
        os.system(f"chmod -R a+w {path}")


@pytest.fixture(scope="session", autouse=True)
def dataset_name():
    return "NEW_BIDS_DS"


@pytest.fixture(scope="session", autouse=True)
def project_name():
    return "NEW_PROJECT"


@pytest.fixture(scope="session", autouse=True)
def public_dataset_name():
    return "PUBLIC_NEW_BIDS_DS"


@pytest.fixture(scope="session", autouse=True)
def dataset_path(dataset_name):
    dataset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tmp", dataset_name)
    )
    if os.path.exists(dataset_path):
        paths = [
            os.path.join(dataset_path, ".git"),
            os.path.join(dataset_path, ".datalad"),
        ]
        for path in paths:
            fix_permissions(path)
        shutil.rmtree(dataset_path)
    return dataset_path


@pytest.fixture(scope="session", autouse=True)
def public_dataset_path(public_dataset_name):
    public_dataset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tmp", "public", public_dataset_name)
    )
    if os.path.exists(public_dataset_path):
        paths = [
            os.path.join(public_dataset_path, ".git"),
            os.path.join(public_dataset_path, ".datalad"),
        ]
        for path in paths:
            fix_permissions(path)
        shutil.rmtree(public_dataset_path)
    return public_dataset_path


@pytest.fixture(scope="session", autouse=True)
def cloned_dataset_path(public_dataset_name):
    cloned_dataset_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "tmp", public_dataset_name)
    )
    if os.path.exists(cloned_dataset_path):
        paths = [
            os.path.join(cloned_dataset_path, ".git"),
            os.path.join(cloned_dataset_path, ".datalad"),
        ]
        for path in paths:
            fix_permissions(path)
        shutil.rmtree(cloned_dataset_path)
    return cloned_dataset_path


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
        paths = [
            os.path.join(project_path, ".git"),
            os.path.join(project_path, ".datalad"),
            os.path.join(project_path, "inputs", "bids-dataset", ".git"),
            os.path.join(project_path, "inputs", "bids-dataset", ".datalad"),
        ]
        for path in paths:
            fix_permissions(path)
        shutil.rmtree(project_path)
    return project_path
