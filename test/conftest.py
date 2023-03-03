# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Define fixtures for testing bids_tools package."""

import os
import pytest


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
    return dataset_path


@pytest.fixture(scope="session", autouse=True)
def io_path():
    io_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp", "io"))
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
    return project_path
