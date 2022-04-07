#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS database using BIDS Manager.
"""

import os
import json
from sre_constants import SUCCESS

# BIDS Manager Python package has to be accessible.
import bids_manager.ins_bids_class as bidsmanager


class DatabaseHandler:

    def __init__(self):
        pass

    def db_create(self, input_data=None, database_path=None):
        """ Create a new BIDS database """
        # Vars
        database_path = os.path.abspath(database_path)
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Init a BIDS Manager DatasetDescJSON dict
        datasetdesc_dict = bidsmanager.DatasetDescJSON()
        # Populate datasetdesc_dict with the data extracted from the create_bids_db.json.
        for bids_key, bids_value in input_data['DatasetDescJSON'].items():
            datasetdesc_dict[bids_key] = bids_value
        # Write the dataset_description.json file only if it does not exist
        db_path = os.path.join(database_path, input_data['database'])
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
        dhdl = DatabaseHandler()
        # dhdl.db_create(input_data=r'../data/input/db_create.json', database_path=r'../data/output')
        # dhdl.db_get(input_data=r'../data/input/db_get.json', output_file=r'../data/output/db_get_out.json')
