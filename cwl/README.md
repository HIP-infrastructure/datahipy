# CWL tools & workflow to manipulate BIDS data


## CWL baseline

`sudo apt-get install cwltool`  

`docker build . -t bids-tools`  


### Dataset
- db.create 

```
cwl-runner --enable-ext cwl/db.create.cwl --input_data=data/input/db_create.json --database_path=data/output
```

- db.get 

```
cwl-runner cwl/db.get.cwl --input_data=data/input/db_get.json
```
