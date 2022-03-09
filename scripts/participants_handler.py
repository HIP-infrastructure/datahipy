#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS participants using BIDS Manager.
"""

import os
import argparse
import json
import shutil
from datetime import datetime

import bids_manager.ins_bids_class as bidsmanager  # BIDS Manager Python package has to be accessible.


class ParticipantHandler:

    #  Those paths shd not be hardcoded but dynamic.
    input_dir = r'C:\...\bids-converter\data\input'  # Path to the input dir
    database_dir = r'C:\...\bids-converter\data\output'  # Path to the BIDS database dir
    importation_dir = r'C:\...\bids-converter\data\importation_directory'  # Path to the importation dir

    def __init__(self):
        pass

    def import_data(self, data_to_import=None):
        """ Add data to an already existing BIDS database """
        # Load the data_to_import json in a dict
        with open(data_to_import, 'r') as f:
            data_to_import = json.load(f)
        # Load the targeted BIDS db in BIDS Manager
        db_content = bidsmanager.BidsDataset(os.path.join(self.database_dir, data_to_import['database']))
        requirements_path = os.path.join(self.database_dir, data_to_import['database'], 'code', 'requirements.json')
        # Init a BIDS Manager data2import dict
        data2import = bidsmanager.Data2Import(data2import_dir=self.importation_dir, requirements_fileloc=requirements_path)
        # Populate the data2import with the data extracted from the dataset_description.json of the BIDS db.
        data2import['DatasetDescJSON'] = db_content['DatasetDescJSON']
        # Populate the data2import with the subjects found in the data_to_import dict
        sub_idx = dict()  # Need to track subject indexes to populate their respective modality dict later
        for idx, subject in enumerate(data_to_import['subjects']):
            new_sub = bidsmanager.Subject()  # Init a BIDS Manager subject dict used for clinical info
            for bids_key, bids_value in subject.items():
                new_sub[bids_key] = bids_value  # Populate the subject dict with the content of the data_to_import dict
            data2import['Subject'].append(new_sub)
            sub_idx[subject['sub']] = idx
        # Populate the data2import with the files found in the data_to_import dict
        for file in data_to_import['files']:
            run = dict()  # Need to track the files being added to the data2import to determine the run number
            # Copy the targeted file in an unique importation dir
            input_file_path = os.path.join(self.input_dir, file['path'])
            file_name = os.path.basename(file['path'])
            token_dir = str(datetime.timestamp(datetime.now())).replace('.', '')  # Suboptimal dir name generation
            output_file_path = os.path.join(os.path.join(self.importation_dir, 'temp_bids'), token_dir, file_name)
            os.makedirs(os.path.dirname(output_file_path))
            shutil.copyfile(input_file_path, output_file_path)
            # Determine the BIDS data type to use and init a BIDS Manager modality dict
            bids_dtype = None
            bids_dtype_dict = dict()
            if file['modality'] in ['T1w', 'T2w', 'CT', 'FLAIR']:
                bids_dtype = 'Anat'
                bids_dtype_dict = bidsmanager.Anat()
            elif file['modality'] in ['ieeg']:
                bids_dtype = 'Ieeg'
                bids_dtype_dict = bidsmanager.Ieeg()
            else:
                pass  # Add other data types here
            # Populate the modality dict with the BIDS entities found in the data_to_import dict
            for bids_key, bids_value in file['entities'].items():
                bids_dtype_dict[bids_key] = bids_value
            bids_dtype_dict['modality'] = file['modality']
            bids_dtype_dict['fileLoc'] = os.path.join('temp_bids', token_dir, file_name)
            entities_str = str(file['entities'].items())  # run dict: key->entities_str, value->run number
            if entities_str not in run:
                run[entities_str] = 1  # Incomplete: need to parse the BIDS db beforehand to determine the starting index
            else:
                run[entities_str] += 1
            bids_dtype_dict['run'] = run[entities_str]
            data2import['Subject'][sub_idx[file['entities']['sub']]][bids_dtype].append(bids_dtype_dict)
        # Saving the data2import now it is populated. Note: subjects without files to import are ignored
        data2import.save_as_json()
        # Importation of the data into the BIDS database using BIDS Manager
        db_content.make_upload_issues(data2import, force_verif=True)
        db_content.import_data(data2import=data2import, keep_sourcedata=True, keep_file_trace=True)  # Create a /sourcedata + source_data_trace.tsv
        db_content.parse_bids()  # Refresh


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(description='BIDS participant handler.')
    parser.add_argument('-data_to_import', help="User data to import in the BIDS db.")
    parser.add_argument('-sub_to_delete', help="BIDS subject to delete from the BIDS db.")
    cmd_args = parser.parse_args()
    data_to_import = cmd_args.data_to_import
    sub_to_delete = cmd_args.sub_to_delete
    # Ins
    phdl = ParticipantHandler()
    if data_to_import:
        phdl.import_data(data_to_import=data_to_import)
    if sub_to_delete:
        pass
