#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Manage BIDS participants using BIDS Manager.
"""

import os
import json
import shutil
from datetime import datetime
from sre_constants import SUCCESS

import bids_manager.ins_bids_class as bidsmanager


class ParticipantHandler:

    # Converter paths in the docker image
    dcm2niix_path = r'/apps/dcm2niix/install/dcm2niix'
    anywave_path = r'anywave'

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

    def sub_delete(self, input_data=None, database_path=None):
        """ Delete a subject from an already existing BIDS database """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS db in BIDS Manager
        db_obj = bidsmanager.BidsDataset(os.path.join(database_path, input_data['database']))
        # Find the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=input_data['subject'])
        # Delete the subject from the BIDS db
        db_obj.remove(sub_dict, with_issues=True, in_deriv=None)  # Will remove from /raw, /source, participants.tsv, source_data_trace.tsv. Not from derivatives
        db_obj.parse_bids()  # Refresh

    def sub_delete_file(self, input_data=None, database_path=None):
        """ Delete a data file of a subject (from /raw and /source) """
        pass  # TODO

    def sub_get(self, input_data=None, database_path=None, output_file=None):
        """ Get info of a subject """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS db in BIDS Manager
        db_obj = bidsmanager.BidsDataset(database_path)
        # Find the info in the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=input_data['info']['sub'])
        sub_info = sub_dict[input_data['info']['dtype']]
        # Dump the sub_info dict in a .json file
        if output_file:
            self.dump_output_file(user=input_data['owner'], output_data=sub_info, output_file=output_file)
        print(SUCCESS)

    def load_input_data(self, input_data):
        """ Load the input_data JSON file """
        with open(input_data, 'r') as f:
            return json.load(f)

    def dump_output_file(self, user=None, output_data=None, output_file=None):
        """ Dump output_data dict in a JSON file """
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)
        # chown created files to user (Docker)
        os.system(f"useradd {user}")
        os.system(f"chown -R {user}:{user} {output_file}")


if __name__ == "__main__":
    if True:
        phdl = ParticipantHandler()
        # phdl.import_data(data_to_import=data_to_import)  # TO DEBUG / IMPROVE
        phdl.sub_delete(input_data=r'../data/input/sub_delete.json',  database_path=r'../data/output')
        phdl.sub_get(input_data=r'../data/input/sub_get.json', database_path=r'../data/output', output_file=r'../data/output/sub_get_out.json')
