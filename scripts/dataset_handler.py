#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS dataset using BIDS Manager.
"""

import os
import json
import re
import pprint as pp
from sre_constants import SUCCESS

import pandas as pd

# BIDS Manager Python package has to be accessible.
import bids_manager.ins_bids_class as bidsmanager
from bids_utils import get_bidsdataset_content


class DatasetHandler:

    def __init__(self, dataset_path=None):
        self.dataset_path = os.path.abspath(dataset_path)

    def dataset_create(self, input_data=None):
        """ Create a new BIDS dataset """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Init a BIDS Manager DatasetDescJSON dict
        datasetdesc_dict = bidsmanager.DatasetDescJSON()
        # Populate datasetdesc_dict with the data extracted from the create_bids_db.json.
        for bids_key, bids_value in input_data['DatasetDescJSON'].items():
            datasetdesc_dict[bids_key] = bids_value
        # Write the dataset_description.json file only if it does not exist
        dataset_name = self.make_safe_filename(input_data['dataset'])
        db_path = os.path.join(self.dataset_path, dataset_name)
        if not os.path.isdir(db_path):
            os.makedirs(db_path)
        datasetdesc_path = os.path.join(db_path, 'dataset_description.json')
        if not os.path.isfile(datasetdesc_path):
            datasetdesc_dict.write_file(jsonfilename=datasetdesc_path)
            # Load the created BIDS dataset in BIDS Manager (creates companion files)
            db_obj = bidsmanager.BidsDataset(db_path)
            if db_obj:
                print('INFO: The dataset_description.json file was updated. BIDS dataset successfully opened')
                if os.path.isdir(db_path):
                    print(SUCCESS)

    def dataset_get(self, input_data=None, output_file=None):
        """ DEPRECIATED - Ask BIDS Manager for some BIDS definitions """

        def get_def_attr(cls):
            """ Local function to extract some info from BIDS Manager classes """
            attr = dict()
            for var, val in vars(cls).items():
                if not var.startswith('_'):
                    if isinstance(val, (str, dict, list)):
                        attr[var] = val
            return attr

        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Fetch the definitions in BIDS Manager classes and store in bids_definitions dict
        bids_definitions = {'BIDS_definitions': dict()}
        for bids_def in input_data['BIDS_definitions']:
            bids_definitions['BIDS_definitions'][bids_def] = get_def_attr(eval('bidsmanager.'+bids_def))
            try:
                bids_def = bids_def + 'JSON'
                bids_definitions['BIDS_definitions'][bids_def] = get_def_attr(eval('bidsmanager.'+bids_def))
            except AttributeError:
                pass  # Ony a few definitions have a companion .json file.
        # Dump the bids_definitions dict in a .json file
        if output_file:
            self.dump_output_file(output_data=bids_definitions, output_file=output_file)
            print(SUCCESS)

    def dataset_get_definitions(self, output_file=None):
        """ Extract BIDS definitions from BIDS Manager """
        import_definitions = dict()
        data_types = bidsmanager.Imaging.get_list_subclasses_names()\
            + bidsmanager.Electrophy.get_list_subclasses_names()\
            + bidsmanager.GlobalSidecars.get_list_subclasses_names()
        nonbids_keys = bidsmanager.BidsJSON.get_list_subclasses_names()\
            + bidsmanager.BidsTSV.get_list_subclasses_names()\
            + bidsmanager.BidsFreeFile.get_list_subclasses_names()\
            + bidsmanager.BidsBrick.required_keys + ['fileLoc'] + ['modality']
        # For each BIDS' data type we populate a dict() with corresponding modalities,
        # input formats (target extension), (required) BIDS entities
        for data_type in data_types:
            import_definitions[data_type] = dict()
            import_definitions[data_type]['modalities'] = getattr(
                bidsmanager, data_type
            ).allowed_modalities
            try:
                import_definitions[data_type]['input_format'] = getattr(
                    bidsmanager, data_type
                ).readable_file_formats
            except AttributeError:
                import_definitions[data_type]['input_format'] = getattr(
                    bidsmanager, data_type
                ).allowed_file_formats
            bm_keys = getattr(bidsmanager, data_type).keylist            
            all_bids_keys = list()
            required_bids_keys = list()
            for bm_key in bm_keys:
                if bm_key not in nonbids_keys:
                    all_bids_keys.append(bm_key)
                    if bm_key in getattr(bidsmanager, data_type).required_keys:
                        required_bids_keys.append(bm_key)  
            import_definitions[data_type]['all_entities'] = all_bids_keys
            import_definitions[data_type]['required_entities'] = required_bids_keys
        # Dump the import_definitions dict in a .json file
        if output_file:
            self.dump_output_file(
                output_data=import_definitions,
                output_file=output_file
            )
            print(SUCCESS)

    def dataset_get_content(self, input_data=None, output_file=None):
        """Extract dataset information indexed by the HIP platform."""
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)

        # Create a disctionary storing the dataset information
        # indexed by the HIP platform
        dataset_desc = get_bidsdataset_content(
            dataset_path=input_data['path'],
            container_dataset_path=self.dataset_path
        )

        # Dump the dataset_desc dict in a .json file
        if output_file:
            self.dump_output_file(
                output_data=dataset_desc,
                output_file=output_file
            )
            print(SUCCESS)

    @staticmethod
    def check_converters(db_obj=None):
        """Check if the converters are specified and (re)write the requirements.json if necessary."""
        # Converter paths in the docker image
        dcm2niix_path = r'/apps/dcm2niix/install/dcm2niix'
        anywave_path = r'/usr/bin/anywave'
        def_converters = {
            'Electrophy': {
                'ext': ['.vhdr', '.vmrk', '.eeg'],
                'path': anywave_path
            },
            'Imaging': {
                'ext': ['.nii'],
                'path': dcm2niix_path
            }
        }
        # Get the requirements.json dict
        req_path = os.path.join(db_obj.dirname, 'code', 'requirements.json')
        req_dict = bidsmanager.Requirements(req_path)
        to_rewrite = False
        if 'Converters' not in req_dict:
            to_rewrite = True
        elif req_dict['Converters'] != def_converters:
            to_rewrite = True
        if to_rewrite:
            # Write the requirements.json
            print('INFO: Updating the requirements.json converters.')
            req_dict['Converters'] = def_converters
            bidsmanager.BidsDataset.dirname = os.path.join(db_obj.dirname)
            req_dict.save_as_json(req_path)
            db_obj.get_requirements()

    @staticmethod
    def get_run(root_dir: str, bids_entities: dict, bids_modality: str):
        """ Parse the BIDS dataset to get the max run for a set of BIDS entities """
        # Generate regexp from entities
        regexp_list = list()
        for bids_key, bids_value in bids_entities.items():
            if bids_value:
                regexp_list.append(f'{bids_key}-{bids_value}')
        regexp_list.append('run-[0-9]{1,3}')
        regexp_list.append(bids_modality)
        regexp_filename = '_'.join(regexp_list)
        # Get run number parsing BIDS
        runs = list()
        for path, directories, files in os.walk(root_dir):
            for file in files:
                if re.search(regexp_filename, file):
                    matched_run = re.search('run-([0-9]{1,3})', file)
                    runs.append(int(matched_run.group(1)))
        runs = sorted(runs)
        if runs:
            return max(runs)
        else:
            return 0

    @staticmethod
    def add_keys_requirements(db_obj=None, clin_keys=None):
        """ Update the requirements.json with new keys """
        for clin_key in clin_keys:
            if clin_key not in db_obj.requirements['Requirements']['Subject']['keys']:
                db_obj.requirements['Requirements']['Subject']['keys'][clin_key] = str()
        db_obj.requirements.save_as_json()

    @staticmethod
    def load_input_data(input_data):
        """ Return input_data JSON file in a dict """
        with open(input_data, 'r') as f:
            return json.load(f)

    @staticmethod
    def dump_output_file(output_data=None, output_file=None):
        """ Dump output_data dict in a JSON file """
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)

    @staticmethod
    def make_safe_filename(s):
        def safe_char(c):
            if c.isalnum():
                return c
            else:
                return "_"
        return "".join(safe_char(c) for c in s).rstrip("_")


def main():
    dhdl = DatasetHandler(dataset_path=r'../data/output')
    dhdl.dataset_get_definitions(output_file=r'../data/output/dataset_get_definitions.json')


if __name__ == "__main__":
    main()
    