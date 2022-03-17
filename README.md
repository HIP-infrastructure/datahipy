# BIDS Converter

Docker container component to convert neuroimaging data to Brain Imaging Data Structure (BIDS)

## Step 1: 
- build the image: `docker build . -t bids-converter`

## Methods

### Database
- db.get  
Get a database with all fields, participants, and existing entities

```
docker run -it --rm \
    -v $(pwd)/data/input:/input \
    -v $(pwd)/data/output:/output \
    -v $(pwd)/scripts:/scripts \
    bids-converter  \
    --command=db.get \
    --input_data=/input/get_bids_def.json \
    --output_file=/output/output.json    
```


- db.schema  
Get the base schema (fields) to create a new BIDS database

- db.create  
Create a new BIDS database

```
docker run -it --rm \
    -v $(pwd)/data/input:/input \
    -v $(pwd)/data/output:/output \
    -v $(pwd)/scripts:/scripts \
    bids-converter  \
    --command=db.create \
    --input_data=/input/create_bids_db.json \
    --database_path=/output/    
```

- db.update  
Update an exiting database. Update existing fields and/or create new fields

## Participant

- sub.create  
Batch create and update participants into an existing BIDS database  

```
docker run -it --rm \
    -v $(pwd)/data/input:/input \
    -v $(pwd)/data/output:/output \
    -v $(pwd)/tmp:/importation_directory \
    -v $(pwd)/scripts:/scripts \
    bids-converter  \
    --command=sub.create \
    --input_data=/input/data_to_import.json \
    --database_path=/output/BIDS_DB 
```

- sub.get  
Get a participan data from a database

```
docker run -it --rm \
    -v $(pwd)/data/input:/input \
    -v $(pwd)/data/output:/output \
    -v $(pwd)/scripts:/scripts \
    bids-converter  \
    --command=sub.get \
    --input_data=/input/get_sub_info.json \
    --database_path=/output/BIDS-DATABASE \
    --output_file=/output/sub.get.json
```

- sub.delete
Remove a participant from a given BIDS database

```
docker run -it --rm \
    -v $(pwd)/data/input:/input \
    -v $(pwd)/data/output:/output \
    -v $(pwd)/scripts:/scripts \
    bids-converter  \
    --command=sub.delete \
    --input_data=/input/get_sub_info.json \
    --database_path=/output/BIDS_DB 
```
