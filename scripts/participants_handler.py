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
    input_dir = '/input' #r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\input'  # Path to the input dir
    #database_dir = r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\output'  # Path to the BIDS database dir
    importation_dir = '/importation_directory' #r'C:\Users\anthony\Documents\GIN\GIT\bids-converter\data\importation_directory'  # Path to the importation dir
    anywave_path = r'C:/AnyWave/AnyWave.exe'  # Path to AnyWave
    dcm2niix_path = r'C:/Users/anthony/Documents/GIN/Softs/dicm2nii/dicm2nii.exe'  # Path to dcm2niix

    def __init__(self):
        pass

    def check_converters(self, db_obj=None):
        """ Check if the converters are specified and (re)write the requirements.json if necessary """
        def_converters = {'Electrophy': {'ext': ['.vhdr', '.vmrk', '.eeg'], 'path': self.anywave_path},
                          'Imaging': {'ext': ['.nii'], 'path': self.dcm2niix_path}}
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
    def find_subject_dict(db_obj=None, subject=None):
        """ Find the subject dict in the parsed BIDS db object """
        matched_sub = [sub_idx for sub_idx, sub_dict in enumerate(db_obj['Subject']) if sub_dict['sub'] == subject]
        if not matched_sub:
            raise IndexError('Could not find the subject in the BIDS db.')
        elif len(matched_sub) > 1:
            raise IndexError('Several subjects with the same ID found in the BIDS db.')
        sub_dict = db_obj['Subject'][matched_sub[0]]
        return sub_dict

    def import_data(self, data_to_import=None, database_path=None):
        """ Add data to an already existing BIDS database """
        # Load the data_to_import json in a dict
        with open(data_to_import, 'r') as f:
            data_to_import = json.load(f)
        # Load the targeted BIDS db in BIDS Manager and check converters
        db_obj = bidsmanager.BidsDataset(database_path)
        self.check_converters(db_obj=db_obj)
        # Init a BIDS Manager data2import dict
        requirements_path = os.path.join(db_obj.dirname, 'code', 'requirements.json')
        data2import = bidsmanager.Data2Import(data2import_dir=self.importation_dir, requirements_fileloc=requirements_path)
        # Populate the data2import with the data extracted from the dataset_description.json of the BIDS db.
        data2import['DatasetDescJSON'] = db_obj['DatasetDescJSON']
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
        db_obj.make_upload_issues(data2import, force_verif=True)
        db_obj.import_data(data2import=data2import, keep_sourcedata=True, keep_file_trace=True)  # Create a /sourcedata + source_data_trace.tsv
        db_obj.parse_bids()  # Refresh

    def del_sub(self, sub_to_delete=None):
        """ Delete a subject from an already existing BIDS database """
        # Load the sub_to_delete json in a dict
        with open(sub_to_delete, 'r') as f:
            sub_to_delete = json.load(f)
        # Load the targeted BIDS db in BIDS Manager
        db_obj = bidsmanager.BidsDataset(os.path.join(self.database_dir, sub_to_delete['database']))
        # Find the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=sub_to_delete['subject'])
        # Delete the subject from the BIDS db
        db_obj.remove(sub_dict, with_issues=True, in_deriv=None)  # Will remove from /raw, /source, participants.tsv, source_data_trace.tsv. Not from derivatives
        db_obj.parse_bids()  # Refresh

    def get_sub_info(self, get_sub_info=None, database_path=None, output_file=None):
        """ Get info of a subject """
        # Load the sub_to_delete json in a dict
        with open(get_sub_info, 'r') as f:
            get_sub_info = json.load(f)
        # Load the targeted BIDS db in BIDS Manager
        db_obj = bidsmanager.BidsDataset(database_path)
        # Find the info in the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=get_sub_info['info']['sub'])
        sub_info = sub_dict[get_sub_info['info']['dtype']]
        # Dump the sub_info dict in a .json file
        with open(output_file, 'w') as f:
            json.dump(sub_info, f, indent=4)


# if __name__ == "__main__":
#     # Args
#     parser = argparse.ArgumentParser(description='BIDS participant handler.')
#     parser.add_argument('-data_to_import', help="User data to import in the BIDS db.")
#     parser.add_argument('-sub_to_delete', help="BIDS subject to delete from the BIDS db.")
#     parser.add_argument('-get_sub_info', help="Get info of a BIDS subject.")
#     cmd_args = parser.parse_args()
#     data_to_import = cmd_args.data_to_import
#     sub_to_delete = cmd_args.sub_to_delete
#     get_sub_info = cmd_args.get_sub_info
#     # Ins
#     phdl = ParticipantHandler()
#     if data_to_import:
#         phdl.import_data(data_to_import=data_to_import)
#     if sub_to_delete:
#         phdl.del_sub(sub_to_delete=sub_to_delete)
#     if get_sub_info:
#         phdl.get_sub_info(get_sub_info=get_sub_info)
