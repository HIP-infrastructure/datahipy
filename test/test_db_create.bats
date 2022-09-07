setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-tools
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/db_create.json 
        {
            "DatasetPath": "${DATASET_NAME}",
            "DatasetDescJSON": {
                "Name": "My New BIDS dataset",
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
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-tools  \
        ${USER} $(id -u $USER) \
        --command=db.create \
        --input_data=/input/db_create.json
        
}

@test 'assert_db_files_exists()' {
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATASET_NAME}
    assert_file_exists ${PROJET_TMP_FOLDER}/${DATASET_NAME}/participants.tsv
    assert_file_exists ${PROJET_TMP_FOLDER}/${DATASET_NAME}/dataset_description.json
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATASET_NAME}/code
    assert_file_exists ${PROJET_TMP_FOLDER}/${DATASET_NAME}/code/requirements.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATASET_NAME}
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATASET_NAME}/participants.tsv
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATASET_NAME}/code
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATASET_NAME}/code/requirements.json
}

@test 'delete files with user ${USER}' {
    # rm ${PROJET_TMP_FOLDER}/db_create.json
}