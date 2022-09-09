#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Script to create and update participants into an existing BIDS dataset.

INPUT
-----

Input folder, passed as a (local)/docker volume contains:
  - data.json which contains:
    - Dataset name and path
    - demographic and clinical data about participants
    - Array of files to import with their associated metadata
  - data folders by participant id, with all files referenced in the JSON files key

OUTPUTS
-------

Output folder, passed as a (local)/docker volume should point to the root file system
  - convert should update existing participants, demographic, clinical data and
    files in dataset/participants.tsv
  - convert should create new participant in dataset
  - convert should update existing participants in their origin folder

EXAMPLES
--------

You can run that script locally as follows::
    $ python3 ./scripts/convert.py data.json

Just make sure you have commented the lines with ``/input`` and ``/output`` and
  uncommented the lines with ``./data/input`` and ``.data/output`` in the folder paths below.
Note also that you will need to have all python dependencies installed including `bids-manager`.
You can check the Dockerfile for more details on the installation of the python environment.

You can use docker-compose to build and run the `bids-tools` image as follows::
    $ docker-compose up

You can alternatively build independently the `bids-tools` image with::
    $ docker build . -t hip/bids-tools

Then, you can run locally the script throughout the docker image as follows:

    ..  code-block:: bash

        $ docker run -it --rm \
            -v $(pwd)/scripts:/scripts \
            -v $(pwd)/data/input:/input \
            -v $(pwd)/data/output:/output \
            hip/bids-tools:latest \
            /scripts/convert.py data.json

On nextcloud, you can run the script throughout the docker image as follows:

    ..  code-block:: bash

        $ docker run -it --rm \
            -v $(pwd)/scripts:/scripts \
            -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/temp/bids-tools/01/:/input \
            -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/files:/output \
            hip/bids-tools:latest \
            /scripts/convert.py data.json

"""

import json
import argparse


def convert(p_data):
    bids_dataset = p_data["dataset"]

    # with open(f"./data/output/{bids_dataset}/output-test.txt", "a") as f:
    with open(f"/output/{bids_dataset}/output-test.txt", "a") as f:
        f.write(json.dumps(p_data))


if __name__ == '__main__':
    # Create parser and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to process")
    args = parser.parse_args()

    # file = f"./data/input/{args.file}"
    file = f"/input/{args.file}"

    with open(file) as json_file:
        data = json.load(json_file)
        convert(data)
