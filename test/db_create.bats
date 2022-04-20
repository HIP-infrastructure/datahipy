export DATABASE_NAME=NEW_BIDS_DB

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'

    PATH=/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin
    # Add BATS test directory to the PATH.
    PATH="$(dirname "${BATS_TEST_DIRNAME}"):$PATH"
}

@test "can build docker image" {
    run docker build $(pwd) -t bids-converter
}

@test "can create input file" {
    cat <<EOT >> test/db_create.json 
        {
            "owner": "${USER}",
            "database": "${DATABASE_NAME}",
            "DatasetDescJSON": {
                "Name": "My New BIDS db",
                "BIDSVersion": "1.4.0",
                "License": "n/a",
                "Authors": [
                    "Tom",
                    "Jerry"
                ],
                "Acknowledgements": "Overwrite test",
                "HowToAcknowledge": "n/a",
                "Funding": "Picsou",
                "ReferencesAndLinks": "n/a",
                "DatasetDOI": "n/a"
            }
        }
EOT
}


@test "can run docker db.create" {
    run docker run -it --rm \
        -v $(pwd)/test:/input \
        -v $(pwd)/test:/output \
        -v $(pwd)/scripts:/scripts \
        bids-converter  \
        --command=db.create \
        --input_data=/input/db_create.json \
        --database_path=/output/   
}

@test 'assert_db_files_exists()' {
    assert_dir_exists test/${DATABASE_NAME}
    assert_file_exists test/${DATABASE_NAME}/participants.tsv
    assert_file_exists test/${DATABASE_NAME}/dataset_description.json
    assert_dir_exists test/${DATABASE_NAME}/code
    assert_file_exists test/${DATABASE_NAME}/code/requirements.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} test/${DATABASE_NAME} 
    assert_file_owner ${USER} test/${DATABASE_NAME}/participants.tsv
    assert_file_owner ${USER} test/${DATABASE_NAME}/code
    assert_file_owner ${USER} test/${DATABASE_NAME}/code/requirements.json
}

@test 'delete files with user ${USER}' {
    rm test/db_create.json
    rm -rf test/${DATABASE_NAME}
}