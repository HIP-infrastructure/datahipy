#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Collection of dictionaries to help for the creation of the data2import.json file used by BIDS Manager for data importation in a BIDS database.
I wrote those dictionaries "by hand" cause it was more convenient at the time, but one shoud probably use BIDS Manager's ins_bids_class module to generate them instead, and get rid of that redundant module. 
The data2import.json file is specific to BIDS Manager and is not related to the BIDS standard per se.
"""

import json
from datetime import datetime

class JsonBlueprints:

    import_json = {'Subject':list(),'Derivatives':list(),'DatasetDescJSON':dict(),'UploadDate':str()}
    
    def __init__(self):
        self.import_json['Derivatives'] = self.generate_derivatives()
        self.import_json['DatasetDescJSON'] = self.generate_datasetdescjson()
        self.import_json['UploadDate'] = self.generate_uploaddate()        
        
    def generate_derivatives(self):
        return list()
    
    def generate_datasetdescjson(self):
        DatasetDescJSON = {
          'Name': 'BIDS_HIP',
          'BIDSVersion': '1.2.0',
          'License': 'n/a',
          'Authors': ['n/a'],
          'Acknowledgements': 'n/a',
          'HowToAcknowledge': 'n/a',
          'Funding': 'n/a',
          'ReferencesAndLinks': 'n/a',
          'DatasetDOI': 'n/a'
        }
        return DatasetDescJSON       
    
    def generate_uploaddate(self):   
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")
        return dt_string 

    @staticmethod
    def write_dict_in_json(import_json,output_file):
        with open(output_file, 'w') as fid:
            json.dump(import_json,fid,indent=1)  
    
    @staticmethod    
    def add_subject(import_json):
        new_subject = {
           'sub': '',
           'Anat': [],
           'Func': [],
           'Fmap': [],
           'Dwi': [],
           'Pet': [],
           'Meg': [],
           'Eeg': [],
           'Ieeg': [],
           'Beh': [],
           'IeegGlobalSidecars': [],
           'EegGlobalSidecars': [],
           'Scans': [],
           'age': '',
           'sex': ''
        }
        import_json['Subject'].append(new_subject)
        return import_json
        
    @staticmethod   
    def new_ieeg_dict():
        seeg_dict = {
            'sub': '',
            'ses': '',
            'task': '',
            'acq': '',
            'run': '',
            'proc': '',
            'modality': 'ieeg',
            'fileLoc': '',
            'IeegJSON': {},
            'IeegChannelsTSV': [],
            'IeegEventsTSV': []
            }    
        return seeg_dict
        
    @staticmethod   
    def new_anat_dict():
        anat_dict = {
            'sub': '',
            'ses': '',
            'acq': '',
            'ce': '',
            'rec': '',
            'run': '',
            "mod": '',
            'modality': '',
            'fileLoc': '',
            'AnatJSON': {},
            }    
        return anat_dict   
    
    @staticmethod   
    def new_pet_dict():
        pet_dict = {
            'sub': '',
            'ses': '',
            'task': '',
            'acq': '',
            'rec': '',
            'run': '',
            'modality': 'pet',
            'fileLoc': '',
            'PetJSON': {},
            }    
        return pet_dict        
        

if __name__ == '__main__':
    pass 