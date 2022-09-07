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

from dataset_handler import DatasetHandler

import bids_manager.ins_bids_class as bidsmanager


class ParticipantHandler:

    def __init__(self, dataset_path=None, input_path=None):
        self.dataset_path = os.path.abspath(dataset_path)
        self.input_path = input_path

    def sub_import(self, input_data=None):
        """ Import subject(s) data into a BIDS dataset """
        # Vars
        runs = dict()  # Track the RUN number of files to import
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager and check converters
        db_obj = bidsmanager.BidsDataset(self.dataset_path)
        DatasetHandler.check_converters(db_obj=db_obj)
        # Add clinical keys to the requirements.json
        clin_keys = list()
        for subject in input_data['subjects']:
            for key in subject:
                if key != 'sub' and key not in clin_keys:
                    clin_keys.append(key)
        DatasetHandler.add_keys_requirements(db_obj=db_obj, clin_keys=clin_keys)
        db_obj.parse_bids()
        # Init importation directory
        import_path = os.path.join('/tmp', 'BIDS_import')
        if os.path.isdir(import_path): shutil.rmtree(import_path)
        if not os.path.isdir(import_path): 
            os.makedirs(import_path)
        # Init a BIDS Manager data2import dict
        requirements_path = os.path.join(db_obj.dirname, 'code', 'requirements.json')
        data2import = bidsmanager.Data2Import(data2import_dir=import_path, requirements_fileloc=requirements_path)
        # Populate the data2import with the data extracted from the dataset_description.json of the BIDS db.
        data2import['DatasetDescJSON'] = db_obj['DatasetDescJSON']
        # Populate the data2import with the subjects found in the data_to_import dict
        sub_idx = dict()  # Need to track subject indexes to populate their respective modality dict later
        for idx, subject in enumerate(input_data['subjects']):
            new_sub = bidsmanager.Subject()  # Init a BIDS Manager subject dict used for clinical info
            for bids_key, bids_value in subject.items():
                new_sub[bids_key] = bids_value  # Populate the subject dict with the content of the data_to_import dict
            data2import['Subject'].append(new_sub)
            sub_idx[subject['sub']] = idx
        # Populate the data2import with the files found in the data_to_import dict
        for file in input_data['files']:
            # Copy the targeted file in a unique importation dir
            file_name = os.path.basename(file['path'])
            file_path = os.path.join(self.input_path, file['path'])
            token_dir = str(datetime.timestamp(datetime.now())).replace('.', '')
            output_file_path = os.path.join(os.path.join(import_path, 'temp_bids'), token_dir, file_name)
            os.makedirs(os.path.dirname(output_file_path))
            shutil.copyfile(file_path, output_file_path)
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
                pass  # Add other BIDS data types here
            # Populate the modality dict with the BIDS entities found in the input_data dict
            for bids_key, bids_value in file['entities'].items():
                bids_dtype_dict[bids_key] = bids_value
            bids_dtype_dict['modality'] = file['modality']
            bids_dtype_dict['fileLoc'] = os.path.join('temp_bids', token_dir, file_name)
            # Determine RUN
            bids_values = tuple(file['entities'].values())
            if bids_values not in runs:
                runs[bids_values] = DatasetHandler.get_run(
                    os.path.join(db_obj.dirname, 'sub-'+file['subject']),
                    file['entities'],
                    file['modality']
                )
            runs[bids_values] += 1
            bids_dtype_dict['run'] = runs[bids_values]
            data2import['Subject'][sub_idx[file['entities']['sub']]][bids_dtype].append(bids_dtype_dict)
        # Saving the data2import now it is populated. Note: subjects without data to import are ignored
        data2import.save_as_json()
        # Importation of the data into the BIDS database using BIDS Manager
        db_obj.make_upload_issues(data2import, force_verif=True)
        db_obj.import_data(data2import=data2import, keep_sourcedata=True, keep_file_trace=True)  # Create a /sourcedata + source_data_trace.tsv
        db_obj.parse_bids()  # Refresh
        print(SUCCESS)

    def sub_delete(self, input_data=None):
        """ Delete a subject from an already existing BIDS dataset """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        db_obj = bidsmanager.BidsDataset(self.dataset_path)
        # Find the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=input_data['subject'])
        db_obj.remove(sub_dict, with_issues=True, in_deriv=None)  # Will remove from /raw, /source, participants.tsv, source_data_trace.tsv. Not from derivatives
        db_obj.parse_bids()  # Refresh
        # Delete the subject from the BIDS dataset

    def sub_delete_file(self, input_data=None):
        """ Delete data files from /raw and /source """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        db_obj = bidsmanager.BidsDataset(self.dataset_path)
        for file in input_data['files']:
            sub_dict = self.find_subject_dict(db_obj=db_obj, subject=file['subject'])
            for file_dict in sub_dict[file['modality']]:
                if file['fullpath'] == file_dict['fileLoc']:
                    db_obj.remove(file_dict, with_issues=True, in_deriv=None)  # Will remove from /raw, /source, source_data_trace.tsv. Not from derivatives
                    print('{} was deleted.'.format(file['fullpath']))
                    print(SUCCESS)

    def sub_get(self, input_data=None, output_file=None):
        """ Get info of a subject """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        db_obj = bidsmanager.BidsDataset(self.dataset_path)
        # Find the info in the subject dict
        sub_dict = self.find_subject_dict(db_obj=db_obj, subject=input_data['sub'])
        sub_info = sub_dict['Anat'] + sub_dict['Ieeg']
        # Dump the sub_info dict in a .json file
        if output_file:
            self.dump_output_file(output_data=sub_info, output_file=output_file)
            print(SUCCESS)

    def sub_edit_clinical(self, input_data=None):
        """ Update subject clinical info in BIDS dataset """
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        db_obj = bidsmanager.BidsDataset(self.dataset_path)
        # Edit subject clinical info
        sub_exists, sub_info, sub_idx = db_obj['ParticipantsTSV'].is_subject_present(input_data['subject'])
        if sub_exists:
            DatasetHandler.add_keys_requirements(
                db_obj=db_obj,
                clin_keys=input_data['clinical'].keys()
            )
            for clin_key, clin_value in input_data['clinical'].items():
                if clin_value:
                    sub_info[clin_key] = clin_value
                else:
                    sub_info[clin_key] = 'n/a'
            del sub_info['sub']
            db_obj.parse_bids()  # To update the participants.tsv with the new columns
            db_obj['ParticipantsTSV'].update_subject(input_data['subject'], sub_info)
            db_obj['ParticipantsTSV'].write_file()
            print(SUCCESS)

    @staticmethod
    def load_input_data(input_data):
        """ Load the input_data JSON file """
        with open(input_data, 'r') as f:
            return json.load(f)

    @staticmethod
    def dump_output_file(output_data=None, output_file=None):
        """ Dump output_data dict in a JSON file """
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)

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


if __name__ == "__main__":
    if True:
        phdl = ParticipantHandler(
            dataset_path=r'../data/output',
            input_path='/home/anthony/Documents/GIT/bids-tools/data/input'
        )  # Do we need input_path here instead of full input path in .json ?
        phdl.sub_import(input_data=r'../input_json_examples/sub_import.json')
        # phdl.sub_delete(input_data=r'../data/input/sub_delete.json',  dataset_path=r'../data/output')
        # phdl.sub_get(
        #   input_data=r'../data/input/sub_get.json',
        #   dataset_path=r'../data/output',
        #   output_file=r'../data/output/sub_get_out.json'
        # )
        # phdl.sub_delete_file(
        #   input_data=r'../data/input/sub_delete_file.json',
        #   dataset_path=r'../data/output'
        # )
        phdl.sub_edit_clinical(input_data=r'../input_json_examples/sub_edit_clinical.json')
