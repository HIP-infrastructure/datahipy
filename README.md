# BIDS Converter

Docker container component to convert neuroimaging data to Brain Imaging Data Structure (BIDS)


## Methods

### Database
- database/get  
Get a database with all fields, participants, and existing entities

- database/schema  
Get the base schema (fields) to create a new BIDS database

- database/create  
Create a new BIDS database

- database/update  
Update an exiting database. Update existing fields and/or create new fields

## Participant

- participant/convert  
Batch create and update participants into an existing BIDS database  
see [convert.py](./scripts/convert.py) for details

- participant/delete
Remove a participant from a given BIDS database


# CWL baseline

`sudo apt-get install cwltool`  

`docker build . -t bids-converter`  

`cwl-runner cwl/bids-convert.cwl --input_command=/scripts/database_handler.py  --input_file=data/input/create_bids_db.json --output_dir=data/output`  
