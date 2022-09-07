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
    files in DatasetPath/participants.tsv
  - convert should create new participant in DatasetPath
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

def convert(data):
    bids_database = data["databasePath"]
    # help(bids_manager)
        $ docker run -it --rm \
            -v $(pwd)/scripts:/scripts \
            -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/temp/bids-tools/01/:/input \
            -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/files:/output \
            hip/bids-tools:latest \
            /scripts/convert.py data.json

    f = open(f"/output/{bids_database}/output-test.txt", "a")
    # f = open(f"./data/output/{bids_database}/output-test.txt", "a")
"""

    f.write(json.dumps(data))
    f.close()
import json
import argparse


def convert(p_data):
    bids_dataset = p_data["datasetPath"]



if __name__ == '__main__':
    # Create parser and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to process")
    args = parser.parse_args()

    # file = f"./data/input/{args.file}"
    f = open(file)
    data = json.load(f)

    convert(data)
    f.close()
