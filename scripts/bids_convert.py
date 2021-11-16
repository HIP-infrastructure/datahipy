#!/usr/bin/python3

import argparse
import bids_manager
import json
import os


# parse arguments
# parser = argparse.ArgumentParser()
# parser.add_argument("test", help="test argument")
# args = parser.parse_args()

# print("Hello " + args.test + "!")

# -*- coding: utf-8 -*-

"""
An example of a script to import some data into a BIDS database using BIDS Manager.

The first step is to move the data we are interested in to a temporary directory that will be used for importation:
-At the root of the temporary directory will reside a data2import.json file that specifies the BIDS pairs to use for each data file to import.
-Inside the temporary directory a subdirectory called "temp_bids" (mandatory) hold the actual copy of all data files about to be imported into the BIDS database.

Once the temporary directory is ready, the script calls a BIDS Manager's class called "ins_bids_class" in order to:
-Initialize a new empty BIDS database.
-Import the data contained inside the temporary directory into the BIDS database using the data2import.json file we carefully created.  
"""

import os
# import secrets # Not on the HIP at the moment but package shd be installed
import time
import shutil
import sys
sys.path.append(r'/usr/local/lib/python3.8/dist-packages/bids_manager-0.3.2-py3.8.egg/bids_manager') # You just need to have BIDS Manager modules in your Python path so you can import ins_bids_class 


import ins_bids_class as BIDS

from json_blueprints import JsonBlueprints # Please see comments in the module


class ImportToBids: # The objective of this class is to create the temporary directory that will be used for the importation of the data into the BIDS database

    # Following lines may seem trivial but it is a critical aspect of the generation of a BIDS database. The user needs to design the BIDS database he is about to generate
    # and choose the data he wants to import. i.e. He decides the demographic and clinical data to use (In that example: age, sex and hospital).
    # He also decides the data files he wants to import (In that example: 1 iEEG and 2 imaging data) and the BIDS pairs he wants to apply on them
    # (for example the iEEG file "Raw_1.TRC" will be renamed using the BIDS pairs "session-postimp" and "task-stimulation",
    # see https://bids-specification.readthedocs.io/en/stable/99-appendices/04-entity-table.html). Thus, the "fake data" below should actually be the output of a guided BIDS designing process
    # available to the user.
    # fake_subject = {'Name':'Toto', 'age':'21', 'sex':'M', 'Hospital':'Somewhere'} # We want to import 1 subject with associated clinical/demographic info
    # fake_ieeg = {'path':r'/data/__groupfolders/1/HIP-test/anthony_tutorial_epimap_brainstorm/seeg/SZ1.TRC', 'session':'postimp', 'task':'stimulation'} # We want to import 1 iEEG file with associated BIDS pairs
    # fake_imaging_dcm = {'path':r'/data/__groupfolders/1/HIP-test/DICOM-HIP-test/MRI-pre-implantation/t1_HIP-test', 'session':'postimp'} # We want to import 1 DICM directory with associated BIDS pairs
    # fake_imaging_nii = {'path':r'/data/__groupfolders/1/HIP-test/anthony_tutorial_epimap_brainstorm/anat/MRI/3DT1post_deface.nii', 'session':'postimp'} # We want to import 1 nii with associated BIDS pairs


    def __init__(self, path_import: str, subject: dict, files: dict):

        self.fake_subject = subject # We want to import 1 subject with associated clinical/demographic info
        self.fake_ieeg = {'path': files['ieeg'], 'session':'postimp', 'task':'stimulation'} # We want to import 1 iEEG file with associated BIDS pairs
        self.fake_imaging_dcm = {'path': files['dcm'], 'session':'postimp'} # We want to import 1 DICM directory with associated BIDS pairs
        self.fake_imaging_nii = {'path': files['nii'], 'session':'postimp'} # We want to import 1 nii with associated BIDS pairs

        self.path_temp = os.path.join(path_import,'temp_bids') # This subdirectory will hold the actual copy of all data files to import
        self.path_json = os.path.join(path_import,'data2import.json') # The path to the soon-to-be-created data2import.json file. Resides at the root of the temporary directory 
        self.import_json = JsonBlueprints().import_json # Please see comments in the module. We basically create an empty data2import dictionary that we are about to populate        
        self.add_subject() # we populate the data2import dictionary with the info/data of 1 subject.
        
    def add_subject(self):
        """ Add a subject to the data2import.json with some iEEG and Imaging data """           
        JsonBlueprints.add_subject(self.import_json)  # add a new subject to the data2import dictionary
        sub_nb = len(self.import_json['Subject'])-1 # Sub_nb is basically the index of the current subject
        # Add clinical/demographic data for the subject
        self.import_json['Subject'][sub_nb]['sub'] = self.fake_subject['Name'].lower()  
        self.import_json['Subject'][sub_nb]['age'] = self.fake_subject['age']
        self.import_json['Subject'][sub_nb]['sex'] = self.fake_subject['sex'] 
        self.import_json['Subject'][sub_nb]['hospital'] = self.fake_subject['Hospital'] 
        # Add iEEG/imaging data for the subject
        self.add_ieeg(sub_nb) # I commented this one as an example
        self.add_imaging_dcm(sub_nb)
        self.add_imaging_nii(sub_nb)
        JsonBlueprints.write_dict_in_json(self.import_json, self.path_json) # Write the populated data2import dictionary into the data2import.json file 
       
    def add_ieeg(self, sub_nb):
        """ Add iEEG data to the subject """
        file_name = os.path.basename(self.fake_ieeg['path']) 
        # token_dir = secrets.token_hex(4) # We are about to copy the iEEG file into the temporary directory and we don't want to overwrite existing data so we use the secrets module to generate an unique token to generate a unique path inside the temporary directory                                 
        token_dir = str(time.time())
        temp_file = os.path.join(self.path_temp, token_dir, file_name) # Unique path for the soon-to-be-copied iEEG file.                       
        ieeg_dict = JsonBlueprints.new_ieeg_dict() # We generate a new empty iEEG dictionary that we are about to populate
        ieeg_dict['sub'] = self.fake_subject['Name'].lower() # BIDS Subject
        ieeg_dict['ses'] = self.fake_ieeg['session'] # BIDS session  
        ieeg_dict['task'] = self.fake_ieeg['task'] # BIDS Task                                   
        ieeg_dict['run'] = 0 # BIDS Run. Identifies files with identical BIDS pairs. It should be determined in accordance to the imported data but also preexisting data inside the BIDS database                      
        ieeg_dict['fileLoc'] = os.path.join('temp_bids', token_dir, file_name) # File location                           
        self.import_json['Subject'][sub_nb]['Ieeg'].append(ieeg_dict) # We append the populated iEEG dictionary to the data2import dictionary
        if not os.path.isdir(os.path.dirname(temp_file)): os.makedirs(os.path.dirname(temp_file))
        shutil.copyfile(self.fake_ieeg['path'], temp_file) # We copy the iEEG file into its unique directory inside the temporary directory
        
    def add_imaging_dcm(self, sub_nb):
        """ Add imaging data (DICOM) to the subject """
        dir_name = os.path.basename(self.fake_imaging_dcm['path']) 
        # token_dir = secrets.token_hex(4)  
        token_dir = str(time.time())
        temp_dir = os.path.join(self.path_temp, token_dir, dir_name) 
        anat_dict = JsonBlueprints.new_anat_dict()   
        anat_dict['sub'] = self.fake_subject['Name'].lower()
        anat_dict['ses'] = self.fake_imaging_dcm['session']
        anat_dict['run'] = 0
        anat_dict['modality'] = 'CT'
        anat_dict['fileLoc'] = os.path.join('temp_bids', token_dir, dir_name)
        self.import_json['Subject'][sub_nb]['Anat'].append(anat_dict)
        if not os.path.isdir(os.path.dirname(temp_dir)): os.makedirs(os.path.dirname(temp_dir))
        shutil.copytree(self.fake_imaging_dcm['path'], temp_dir)      
        
    def add_imaging_nii(self, sub_nb):
        """ Add imaging (NIfTI) data to the subject """
        file_name = os.path.basename(self.fake_imaging_nii['path']) 
        # token_dir = secrets.token_hex(4)  
        token_dir = str(time.time())
        temp_file = os.path.join(self.path_temp, token_dir, file_name) 
        anat_dict = JsonBlueprints.new_anat_dict()   
        anat_dict['sub'] = self.fake_subject['Name'].lower()
        anat_dict['ses'] = self.fake_imaging_nii['session']
        anat_dict['run'] = 0
        anat_dict['modality'] = 'CT'
        anat_dict['fileLoc'] = os.path.join('temp_bids', token_dir, file_name)
        self.import_json['Subject'][sub_nb]['Anat'].append(anat_dict)
        if not os.path.isdir(os.path.dirname(temp_file)): os.makedirs(os.path.dirname(temp_file))
        shutil.copyfile(self.fake_imaging_nii['path'], temp_file)         
                                        
def convert(data):
    print(json.dumps(data))
    
    user_path = f"/data/{data['owner']}/files"
    
    user_path_bids_db = f"{user_path}/BIDS-Subjects"
    os.makedirs(user_path_bids_db, exist_ok=True)

    path_import = f"{user_path}/tmp/{data['name']}" # This is the path of the temporary directory that will be used for importation
    os.makedirs(path_import, exist_ok=True)

    subject = { 'Name': data['name'],  'age': data['age'],  'sex': data['sex'], 'Hospital': 'Anywhere'}
    files = { 
        'ieeg': f"{user_path}{data['ieeg']}", 
        'dcm': f"{user_path}{data['imaging']['dcm']}",
        'nii': f"{user_path}{data['imaging']['nii']}"
    }
    
    ImportToBids(path_import, subject, files) # Create the data2import.json and transfer the data to import into the temporary directory
    if True:        
        # At this point, we have our temporary directory and associated data2import.json file ready
        # Initialize a new BIDS database     
        path_bids_db = user_path_bids_db # Path to the directory that will hold the BIDS database we are about to generate
        requirements_file = r'/scripts/requirements.json' # The requirements.json is a mandatory master file for BIDS Manager and should, at least, contain the expected demographic
        # and clinical values for the subjects. During the importation process the specified values will populate the participants.tsv file that can be found at the root of the BIDS database.
        # Optimally, the requirements.json should also specify all the expected/optional data to be found inside the BIDS database for BIDS Manager to work fully.
        ieeg_converter = r'/usr/bin/anywave' # Path to AnyWave executable
        imaging_converter = r'/apps/dcm2niix/install/dcm2niix' # Path to dcm2niix executable
        protocol_name = r'BIDS_HIP' # Basically the name of the BIDS database. This info will be stored into the mandatory dataset_description.json file at the root of the BIDS database. The
        # data2import.json needs to use the same name or else BIDS Manager will tell you you are not importing data into the right BIDS database 
        req_dict = BIDS.Requirements(requirements_file)
        BIDS.BidsDataset.converters['Imaging']['path'] = imaging_converter
        req_dict['Converters']['Imaging']['path'] = imaging_converter   
        BIDS.BidsDataset.converters['Electrophy']['path'] = ieeg_converter
        req_dict['Converters']['Electrophy']['path'] = ieeg_converter
        BIDS.BidsDataset.dirname = path_bids_db
        req_dict.save_as_json(os.path.join(BIDS.BidsDataset.dirname, 'code', 'requirements.json'))
        datasetDes = BIDS.DatasetDescJSON()
        datasetDes['Name'] = protocol_name
        datasetDes.write_file() # At this point the new BIDS database is generated and ready for some data.
        # Import data in the new BIDS database
        curr_bids = BIDS.BidsDataset(path_bids_db)
        curr_data2import = BIDS.Data2Import(path_import, os.path.join(path_bids_db, 'code', 'requirements.json')) # Here we specify the temporary directory we carefully prepared 
        # and BIDS Manager will find all it needs to start the importation. i.e. the copied data files and associated data2import.json file   
        curr_bids.make_upload_issues(curr_data2import, force_verif=True)
        curr_bids.import_data(data2import=curr_data2import, keep_sourcedata=True, keep_file_trace=True)
        curr_bids.parse_bids() #requires BIDS validator  

if __name__ == '__main__':
    data = json.loads("""{
        "ieeg": "/mysubject/SZ1.TRC",
        "imaging": {
            "dcm": "/mysubject/t1_HIP-test",
            "nii": "/mysubject/3DT1post_deface.nii"
        },
        "name": "78",
        "age": "zz",
        "sex": "55",
        "owner": "mspuhler"
        }""")
    convert(data)
    