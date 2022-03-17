#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS database using BIDS Manager.
"""

import os
import argparse
import json
from sre_constants import SUCCESS

# BIDS Manager Python package has to be accessible.
import bids_manager.ins_bids_class as bidsmanager


class DatabaseHandler:

    #  Those paths shd not be hardcoded but dynamic.
    # Path to the input dir
    input_dir = r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\input'
    # Path to the BIDS database dir
    database_dir = r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\output'
    # Path to the importation dir
    importation_dir = r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\importation_directory'
    anywave_path = r'C:/AnyWave/AnyWave.exe'  # Path to AnyWave
    # Path to dcm2niix
    dcm2niix_path = r'C:/Users/anthony/Documents/GIN/Softs/dicm2nii/dicm2nii.exe'

    def __init__(self):
        pass

    def create_bids_db(self, create_bids_db=None, database_path=None):
        """ Create a new BIDS database """
        # Load the create_bids_db json in a dict
        with open(create_bids_db, 'r') as f:
            create_bids_db = json.load(f)

        # Init a BIDS Manager DatasetDescJSON dict
        datasetdesc_dict = bidsmanager.DatasetDescJSON()
        # Populate datasetdesc_dict with the data extracted from the create_bids_db.json.
        for bids_key, bids_value in create_bids_db['DatasetDescJSON'].items():
            datasetdesc_dict[bids_key] = bids_value
        # Write the dataset_description.json file only if it does not exist
        db_path = os.path.join(database_path, create_bids_db['database'])
        if not os.path.isdir(db_path):
            os.makedirs(db_path)
        datasetdesc_path = os.path.join(db_path, 'dataset_description.json')
        if not os.path.isfile(datasetdesc_path):
            datasetdesc_dict.write_file(jsonfilename=datasetdesc_path)
            # Load the created BIDS db in BIDS Manager (creates companion files)
            db_obj = bidsmanager.BidsDataset(db_path)
            if db_obj:
                print(
                    'INFO: The dataset_description.json file was updated. BIDS db successfully opened')

    @staticmethod
    def get_bids_def(get_bids_def=None, output_file=None):
        """ Ask BIDS Manager for some BIDS definitions """

        def get_def_attr(cls):
            """ Local function to extract some info from BIDS Manager classes """
            attr = dict()
            for var, val in vars(cls).items():
                if not var.startswith('_'):
                    if isinstance(val, (str, dict, list)):
                        attr[var] = val
            return attr

        # Load the get_bids_def json in a dict
        with open(get_bids_def, 'r') as f:
            get_bids_def = json.load(f)
        # Fetch the definitions in BIDS Manager classes and store in bids_definitions dict
        bids_definitions = {'BIDS_definitions': dict()}
        for bids_def in get_bids_def['BIDS_definitions']:
            bids_definitions['BIDS_definitions'][bids_def] = get_def_attr(
                eval('bidsmanager.'+bids_def))
            try:
                bids_def = bids_def+'JSON'
                bids_definitions['BIDS_definitions'][bids_def] = get_def_attr(
                    eval('bidsmanager.'+bids_def))
            except AttributeError:
                pass  # Ony a few definitions have a companion .json file.
        # Dump the bids_definitions dict in a .json file

        if (output_file):
            with open(output_file, 'w') as f:
                json.dump(bids_definitions, f, indent=4)
                   # chown created files to user (Docker)
            user = get_bids_def['owner']
            os.system(f"useradd {user}")
            os.system(f"chown -R {user}:{user} {output_file}")
        else:
            return (json.dump(bids_definitions, f, indent=4))

        print(SUCCESS)

 


# if __name__ == "__main__":
#     # Args
#     parser = argparse.ArgumentParser(description='BIDS database handler.')
#     parser.add_argument('-create_bids_db', help="Create a new BIDS database.")
#     parser.add_argument('--output_directory', help="Get BIDS output folder")
#     parser.add_argument('-get_bids_def', help="Get BIDS definitions from BIDS Manager.")

#     cmd_args = parser.parse_args()
#     create_bids_db = cmd_args.create_bids_db
#     output_directory = cmd_args.output_directory
#     get_bids_def = cmd_args.get_bids_def

#     print (cmd_args)
#     print (create_bids_db)
#     print(output_directory)

#     # Ins
#     dhdl = DatabaseHandler()
#     if create_bids_db:
#         dhdl.create_bids_db(create_bids_db=create_bids_db,
#                             database_path=output_directory)
#     if get_bids_def:
#         dhdl.get_bids_def(get_bids_def=get_bids_def)
