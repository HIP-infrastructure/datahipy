#!/usr/bin/env python

# Copyright (C) 2022, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""`Setup.py` for datahipy."""
from os import path as op
from setuptools import setup
from datahipy.info import __version__


def main():
    """Main function of datahipy ``setup.py``"""
    root_dir = op.abspath(op.dirname(__file__))

    version = None
    cmdclass = {}
    if op.isfile(op.join(root_dir, "datahipy", "VERSION")):
        with open(op.join(root_dir, "datahipy", "VERSION")) as vfile:
            version = vfile.readline().strip()

    if version is None:
        version = __version__

    # Setup configuration
    setup(
        name="datahipy",
        version=version,
        cmdclass=cmdclass,
    )


if __name__ == "__main__":
    main()
