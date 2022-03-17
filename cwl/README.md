# CWL tools & workflow to manipulate BIDS data


## CWL baseline

`sudo apt-get install cwltool`  

`docker build . -t bids-converter`  


### Database
- db.create 

```
cwl-runner --enable-ext cwl/db.create.cwl --input_data=data/input/create_bids_db.json --database_path=data/output
```

- db.get 

```
cwl-runner cwl/db.get.cwl --input_data=data/input/get_sub_info.json
```
