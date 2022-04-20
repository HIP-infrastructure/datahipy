export DATABASE_NAME=BIDS_DB

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
    cat <<EOT >> test/sub_import.json 
        {
    "owner": "${USER}",
    "database": "${DATABASE_NAME}",
    "subjects": [{
        "sub": "carole",
        "age": "25",
        "sex": "M",
        "hospital": "CHUV"
    }],
    "files": [{
            "modality": "ieeg",
            "subject": "carole",
            "path": "/home/anthony/Documents/GIT/bids-converter/data/input/sub-carole/SZ1.TRC",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "task": "stimulation",
                "acq": "1024hz"
            }
        },
        {
            "modality": "ieeg",
            "subject": "carole",
            "path": "/home/anthony/Documents/GIT/bids-converter/data/input/sub-carole/SZ2.TRC",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "task": "stimulation",
                "acq": "1024hz"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "/home/anthony/Documents/GIT/bids-converter/data/input/sub-carole/3DT1post_deface.nii",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "acq": "lowres",
                "ce": "gadolinium"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "/home/anthony/Documents/GIT/bids-converter/data/input/sub-carole/3DT1post_deface_2.nii",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "acq": "lowres",
                "ce": "gadolinium"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "/home/anthony/Documents/GIT/bids-converter/data/input/sub-carole/3DT1pre_deface.nii",
            "entities": {
                "sub": "carole",
                "ses": "preimp",
                "acq": "lowres"
            }
        }
    ]
}
EOT
}


@test "can run docker sub.import" {
    run docker run -it --rm \
        -v $(pwd)/test:/input \
        -v $(pwd)/test:/output \
        -v $(pwd)/tmp:/importation_directory \
        -v $(pwd)/scripts:/scripts \
        bids-converter  \
        --command=sub.import \
        --input_data=/input/sub_import.json \
        --database_path=/output/testdata/bidsdatabase/BIDS_DB
}

# @test 'assert_db_files_exists()' {
#     assert_dir_exists test/${DATABASE_NAME}
#     assert_file_exists test/${DATABASE_NAME}/participants.tsv
#     assert_file_exists test/${DATABASE_NAME}/dataset_description.json
#     assert_dir_exists test/${DATABASE_NAME}/code
#     assert_file_exists test/${DATABASE_NAME}/code/requirements.json
# }

# @test 'assert_file_owner()' {
#     assert_file_owner ${USER} test/${DATABASE_NAME} 
#     assert_file_owner ${USER} test/${DATABASE_NAME}/participants.tsv
#     assert_file_owner ${USER} test/${DATABASE_NAME}/code
#     assert_file_owner ${USER} test/${DATABASE_NAME}/code/requirements.json
# }

# @test 'delete files with user ${USER}' {
#     rm test/db_create.json
#     rm -rf test/${DATABASE_NAME}
# }