# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Test the datahipy CLI --help / -h command."""

from __future__ import absolute_import
import pytest
from datalad.support.gitrepo import GitRepo


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order("first")
def test_run_help(script_runner):
    ret = script_runner.run("datahipy", "-h")
    assert ret.success
