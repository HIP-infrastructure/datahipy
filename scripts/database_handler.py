#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS database using BIDS Manager.
"""

import os
import json
import re
from sre_constants import SUCCESS

# BIDS Manager Python package has to be accessible.
import bids_manager.ins_bids_class as bidsmanager


class DatabaseHandler:

    def __init__(self, database_path=None):
        self.database_path = os.path.abspath(database_path)

    def db_create(self, input_data=None):
        """ Create a new BIDS database """
        # Vars
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        user = input_data['owner']
        # Init a BIDS Manager DatasetDescJSON dict
        datasetdesc_dict = bidsmanager.DatasetDescJSON()
        # Populate datasetdesc_dict with the data extracted from the create_bids_db.json.
        for bids_key, bids_value in input_data['DatasetDescJSON'].items():
            datasetdesc_dict[bids_key] = bids_value
        # Write the dataset_description.json file only if it does not exist
        db_path = os.path.join(self.database_path, input_data['database'].replace(" ", ""))
        if not os.path.isdir(db_path):
            os.makedirs(db_path)
        datasetdesc_path = os.path.join(db_path, 'dataset_description.json')
        if not os.path.isfile(datasetdesc_path):
            datasetdesc_dict.write_file(jsonfilename=datasetdesc_path)
            # Load the created BIDS db in BIDS Manager (creates companion files)
            db_obj = bidsmanager.BidsDataset(db_path)
            if db_obj:
                print('INFO: The dataset_description.json file was updated. BIDS db successfully opened')
                print(SUCCESS)
        # Chown form root to user
        if os.path.isdir(db_path):
            os.system(f"useradd {user}")
            os.system(f"chown -R {user}:{user} {db_path}")

    def db_get(self, input_data=None, output_file=None):
        """ Ask BIDS Manager for some BIDS definitions """

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
                bids_def = bids_def+'JSON'
                bids_definitions['BIDS_definitions'][bids_def] = get_def_attr(eval('bidsmanager.'+bids_def))
            except AttributeError:
                pass  # Ony a few definitions have a companion .json file.
        # Dump the bids_definitions dict in a .json file
        if output_file:
            self.dump_output_file(user=input_data['owner'], output_data=bids_definitions, output_file=output_file)
        print(SUCCESS)

    @staticmethod
    def check_converters(db_obj=None):
        """ Check if the converters are specified and (re)write the requirements.json if necessary """
        # Converter paths in the docker image
        dcm2niix_path = r'/apps/dcm2niix/install/dcm2niix'
        anywave_path = r'/usr/bin/anywave'
        def_converters = {'Electrophy': {'ext': ['.vhdr', '.vmrk', '.eeg'], 'path': anywave_path},
                          'Imaging': {'ext': ['.nii'], 'path': dcm2niix_path}}
        req_path = os.path.join(db_obj.dirname, 'code', 'requirements.json')
        req_dict = bidsmanager.Requirements(req_path)  # Get the requirements.json dict
        to_rewrite = False
        if 'Converters' not in req_dict:
            to_rewrite = True
        elif req_dict['Converters'] != def_converters:
            to_rewrite = True
        if to_rewrite:
            print('INFO: Updating the requirements.json converters.')
            req_dict['Converters'] = def_converters
            bidsmanager.BidsDataset.dirname = os.path.join(db_obj.dirname)
            req_dict.save_as_json(req_path)  # Write the requirements.json
            db_obj.get_requirements()

    @staticmethod
    def get_run(root_dir: str, bids_entities: dict, bids_modality: str):
        """ Parse the BIDS database to get the max run for a set of BIDS entities """
        # Generate regexp from entities
        regexp_list = list()
        for bids_key, bids_value in bids_entities.items():
            if bids_value:
                regexp_list.append('{}-{}'.format(bids_key, bids_value))
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
    def dump_output_file(user=None, output_data=None, output_file=None):
        """ Dump output_data dict in a JSON file """
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)
        # chown created files to user (Docker)
        os.system(f"useradd {user}")
        os.system(f"chown -R {user}:{user} {output_file}")


if __name__ == "__main__":
    if True:
        dhdl = DatabaseHandler(database_path=r'../data/output')
        dhdl.db_create(input_data=r'../input_json_examples/db_create.json')
        # dhdl.db_get(input_data=r'../data/input/db_get.json', output_file=r'../data/output/db_get_out.json')
