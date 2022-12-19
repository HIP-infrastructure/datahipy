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

## Methods

### Dataset

#### dataset.get  
Get a dataset with all fields, participants, and existing entities 
- [see test/db_get.bats](test/db_get.bats)


#### dataset.create  
Create a new BIDS dataset
- [see test/db_create.bats](test/db_create.bats)


## Participant

#### sub.import  
Import and update participant into an existing BIDS dataset  
- [see test/sub_import.bats](test/sub_import.bats)

#### sub.get  
Get a participan data from a dataset

- [see test/sub_get.bats](test/sub_get.bats)

#### sub.delete  
Remove a participant from a given BIDS dataset

#### sub.delete.file  
Remove data file(s) from a BIDS dataset
