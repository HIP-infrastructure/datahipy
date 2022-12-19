#!/usr/bin/env python

"""`Setup.py` for bids_tools."""

import os
import setuptools
from bids_tools.info import __version__

# Get directory where this file is located
directory = os.path.abspath(os.path.dirname(__file__))

# Remove any MANIFEST of a previous installation
if os.path.exists("MANIFEST"):
    os.remove("MANIFEST")

# Define the packages to be installed
packages = [
    "bids_tools",
    "bids_tools.cli",
    "bids_tools.bids",
    "bids_tools.handlers",
]

# Define the package data to be installed
package_data = {
    "bids_tools.bids": [
        "config/*.json",
    ],
}


# Read the contents of your README file
with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def main():
    """Main function of bids_tools ``setup.py``"""
    # Setup configuration
    setuptools.setup(
        name="bids_tools",
        version=__version__,
        description="bids_tools: Tools to manage BIDS datasets in the Human intracranial EEG platform",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="The HIP team",
        author_email="support@hip.ch",
        url="https://github.com/HIP-infrastructure/bids-converter",
        entry_points={
            "console_scripts": [
                "bids_tools = bids_tools.cli.main:main",
            ]
        },
        license="BSD-3-Clause",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3.7",
        ],
        maintainer="The HIP team",
        maintainer_email="support@hip.ch",
        packages=packages,
        include_package_data=True,
        package_data=package_data,
        requires=["pybids (>=0.15.3)"],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    main()
