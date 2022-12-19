# `bids_tools`: Tools to manage BIDS datasets in the Human intracranial EEG platform

`bids_tools` is a docker container component to handle neuroimaging data on the Human Intracranial EEG Platform (HIP) following Brain Imaging Data Structure ([BIDS](https://bids-specification.readthedocs.io)).

## Installation:
This tool can be easily installed as follows:
- Clone this repository 
- Checkout submodules:
  - `git submodule update --recursive --init`
- build the image: `docker build -t bids-tools .`

## Test
- run `test/run_tests.sh`

## Usage

The tool can be easily run as follows:

```output
usage: bids_tools [-h]
                  [--command {dataset.create,dataset.get,datasets.get,sub.get,sub.import,sub.edit.clinical,sub.delete,sub.delete.file}]
                  [--input_data INPUT_DATA]
                  [--output_file OUTPUT_FILE]
                  [--dataset_path DATASET_PATH]
                  [--input_path INPUT_PATH] [-v]

BIDS dataset handler.

optional arguments:
  -h, --help            show this help message and exit
  --command {dataset.create,dataset.get,datasets.get,sub.get,sub.import,sub.edit.clinical,sub.delete,sub.delete.file}
                        Method to be run.
  --input_data INPUT_DATA
                        Input JSON data
  --output_file OUTPUT_FILE
                        File location after processing
  --dataset_path DATASET_PATH
                        Path to the dataset
  --input_path INPUT_PATH
                        Path to the input data (e.g.
                        input_data.json)
  -v, --version         show program's version number and
                        exit
```

## Commands

### Dataset

#### `dataset.get`  
Get a JSON summary of dataset consisting of all fields, participants, and existing entities.

#### `dataset.create ` 
Create a new BIDS dataset.

## Participant

#### `sub.import`
Import and update files for a given participant into an existing BIDS dataset. An appropriate record is added/updated to the ``participants.tsv`` tabular file if needed.

#### `sub.get`
Get information about data available for a given participant of a dataset.

#### `sub.edit.clinical`
Edit the participant's information stored in the ``participants.tsv`` tabular file.

#### `sub.delete`
Remove a participant from a given BIDS dataset. The record will be deleted from the ``participants.tsv`` tabular file.

#### `sub.delete.file`
Remove data file(s) from a BIDS dataset.
