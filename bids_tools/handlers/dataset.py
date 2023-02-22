# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Manage BIDS dataset using BIDS Manager."""

import os
import json
import re
from sre_constants import SUCCESS

# BIDS Manager Python package has to be accessible.
try:
    from bids_manager.ins_bids_class import (
        BidsDataset,
        Requirements,
        DatasetDescJSON,
    )
except ImportError:
    print("WARNING: BIDS Manager Python package is not accessible.")

from bids_tools.bids.dataset import get_bidsdataset_content


class DatasetHandler:
    def __init__(self, dataset_path=None):
        self.dataset_path = os.path.abspath(dataset_path)

    def dataset_create(self, input_data=None):
        """Create a new BIDS dataset."""
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Init a BIDS Manager DatasetDescJSON dict
        datasetdesc_dict = DatasetDescJSON()
        # Populate datasetdesc_dict with the data extracted from the create_bids_db.json.
        for bids_key, bids_value in input_data["DatasetDescJSON"].items():
            datasetdesc_dict[bids_key] = bids_value
        # Write the dataset_description.json file only if it does not exist
        dataset_name = self.make_safe_filename(input_data["dataset_dirname"])
        ds_path = os.path.join(self.dataset_path, dataset_name)
        if not os.path.isdir(ds_path):
            os.makedirs(ds_path)
        datasetdesc_path = os.path.join(ds_path, "dataset_description.json")
        if not os.path.isfile(datasetdesc_path):
            datasetdesc_dict.write_file(jsonfilename=datasetdesc_path)
            # Load the created BIDS dataset in BIDS Manager (creates companion files)
            ds_obj = BidsDataset(ds_path)
            if ds_obj:
                print(
                    "INFO: The dataset_description.json file was updated. "
                    "BIDS dataset successfully opened"
                )
                if os.path.isdir(ds_path):
                    print(SUCCESS)

    def dataset_get_content(self, input_data=None, output_file=None):
        """Extract dataset information indexed by the HIP platform."""
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)

        # Create a disctionary storing the dataset information
        # indexed by the HIP platform
        dataset_desc = get_bidsdataset_content(bids_dir=self.dataset_path)

        # Dump the dataset_desc dict in a .json file
        if output_file:
            self.dump_output_file(
                output_data=dataset_desc, output_file=output_file
            )
            print(SUCCESS)

    @staticmethod
    def check_converters(ds_obj=None):
        """Check if the converters are specified and (re)write the requirements.json if necessary."""
        # Converter paths in the docker image
        dcm2niix_path = r"/apps/dcm2niix/install/dcm2niix"
        anywave_path = r"/usr/bin/anywave"
        def_converters = {
            "Electrophy": {
                "ext": [".vhdr", ".vmrk", ".eeg"],
                "path": anywave_path,
            },
            "Imaging": {"ext": [".nii"], "path": dcm2niix_path},
        }
        # Get the requirements.json dict
        req_path = os.path.join(ds_obj.dirname, "code", "requirements.json")
        req_dict = Requirements(req_path)
        to_rewrite = False
        if ("Converters" not in req_dict) or (
            req_dict["Converters"] != def_converters
        ):
            to_rewrite = True
        if to_rewrite:
            # Write the requirements.json
            print("INFO: Updating the requirements.json converters.")
            req_dict["Converters"] = def_converters
            BidsDataset.dirname = os.path.join(ds_obj.dirname)
            req_dict.save_as_json(req_path)
            ds_obj.get_requirements()

    @staticmethod
    def get_run(root_dir: str, bids_entities: dict, bids_modality: str):
        """Parse the BIDS dataset to get the max run for a set of BIDS entities."""
        # Generate regexp from entities
        regexp_list = list()
        for bids_key, bids_value in bids_entities.items():
            if bids_value:
                regexp_list.append(f"{bids_key}-{bids_value}")
        regexp_list.append("run-[0-9]{1,3}")
        regexp_list.append(bids_modality)
        regexp_filename = "_".join(regexp_list)
        # Get run number parsing BIDS
        runs = list()
        for path, directories, files in os.walk(root_dir):
            for file in files:
                if re.search(regexp_filename, file):
                    matched_run = re.search("run-([0-9]{1,3})", file)
                    runs.append(int(matched_run.group(1)))
        runs = sorted(runs)
        if runs:
            return max(runs)
        else:
            return 0

    @staticmethod
    def add_keys_requirements(ds_obj=None, clin_keys=None):
        """Update the requirements.json with new keys."""
        for clin_key in clin_keys:
            if (
                clin_key
                not in ds_obj.requirements["Requirements"]["Subject"]["keys"]
            ):
                ds_obj.requirements["Requirements"]["Subject"]["keys"][
                    clin_key
                ] = str()
        ds_obj.requirements.save_as_json()

    @staticmethod
    def load_input_data(input_data):
        """Return input_data JSON file in a dict."""
        with open(input_data, "r") as f:
            return json.load(f)

    @staticmethod
    def dump_output_file(output_data=None, output_file=None):
        """Dump output_data dict in a JSON file."""
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4)

    @staticmethod
    def make_safe_filename(s):
        def safe_char(c):
            if c.isalnum():
                return c
            else:
                return "_"

        return "".join(safe_char(c) for c in s).rstrip("_")
