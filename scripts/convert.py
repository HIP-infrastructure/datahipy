#!/usr/bin/python3

import argparse
#import bids_manager
import json
import os
import argparse

# Script to create and update participants into an existing BIDS database

# INPUT
# input folder, passed as a (local)/docker volume contains:
# JSON file: data.json which contains
#   - Database name and path
#   - demographic and clinical data about participants
#   - Array of files to import with their associated metadata
# /data folder with all files referenced in files

# OUTPUT
# output folder, passed as a (local)/docker volume should point to the root file system
# Should update existing participants, demographic, clinical data and files in databasePath/participants.tsv
# Should create new participant in databasePath

"""
You can run that script locally, just make sure that you change
/input and /output in ./data/input and .data/output in the folders path below

run with: 
python3 ./scripts/convert.py data.json


examples for docker, or run 
docker-compose up

build:
docker build . -t hip/bids-converter 

run: 
docker run -it --rm -v $(pwd)/scripts:/scripts -v $(pwd)/data/input:/input -v $(pwd)/data/output:/output hip/bids-converter:latest /scripts/convert.py data.json

run for nextcloud: 
docker run -it --rm -v $(pwd)/scripts:/scripts -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/temp/bids-converter/01/:/input -v /mnt/nextcloud-dp/nextcloud/data/mspuhler/files:/output hip/bids-converter:latest /scripts/convert.py data.json

"""

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to process")
args = parser.parse_args()

# -*- coding: utf-8 -*-


def convert(data):
    bids_database = data["databasePath"]
    # help(bids_manager)

    f = open(f"/output/{bids_database}/output-test.txt", "a")
    # f = open(f"./data/output/{bids_database}/output-test.txt", "a")

    f.write(json.dumps(data))
    f.close()


if __name__ == '__main__':
    file = f"/input/{args.file}"
    # file = f"./data/input/{args.file}"
    f = open(file)
    data = json.load(f)

    convert(data)
    f.close()
