# `bids_tools`: Tools to manage BIDS datasets in the Human intracranial EEG platform
---

Copyright © 2012-2023 The HIP team and Contributors, All rights reserved.

This software is distributed under the open-source Apache 2.0 license. See [LICENSE](LICENSE.txt) file for details.

---
[![CI/CD](https://gitlab.hbp.link/hip/bids-tools/badges/master/pipeline.svg)](https://gitlab.hbp.link/hip/bids-tools/-/commits/master) [![Coverage](https://gitlab.hbp.link/hip/bids-tools/badges/master/coverage.svg)](https://gitlab.hbp.link/hip/bids-tools/-/commits/master)

`bids_tools` is an open-source tool written in Python and encapsulated in a Docker image to handle neuroimaging data on the Human Intracranial EEG Platform (HIP) following Brain Imaging Data Structure ([BIDS](https://bids-specification.readthedocs.io)).

### Resources

*   **Documentation:** https://hip-infrastructure.github.io/bids-converter/
*   **Source:** https://github.com/HIP-infrastructure/bids-converter
*   **Bug reports:** https://github.com/HIP-infrastructure/bids-converter/issues

## Installation

*   Install Docker engine (See [instructions](https://hip-infrastructure.github.io/bids-converter/installation.html#installation-of-docker-engine))

*   Clone this repository:

    ```bash
    $ git clone https://github.com/HIP-infrastructure/bids-converter.git bids-tools
    ```

*   Go to your local clone folder and build the Docker image:

     ```bash
    $ cd bids-tools
    $ make -B build-docker
    ```

*   You are ready to use `bids_tools` :rocket:!

## Test
Run `test/run_tests.sh` in a terminal:
```bash
$ sh test/run_tests.sh
```
After completion, coverage report in HTML format can be found in ``test/report/cov_html`` and be displayed by opening ``index.html`` in your favorite browser.

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
