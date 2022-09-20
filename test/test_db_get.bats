setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-tools
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/db_get.json 
        {
            "BIDS_definitions": ["Anat", "Ieeg", "DatasetDescJSON"]
        }
EOT
}


@test "can run docker db.get" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}/${DATASET_NAME}:/output \
        -v ${PROJET_TMP_FOLDER}:/file \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-tools  \
        ${USER} $(id -u $USER) \
        --command=db.get \
        --input_data=/input/db_get.json \
        --output_file=/file/output.json      
}

@test 'assert_file_contains()' {
    assert_file_contains ${PROJET_TMP_FOLDER}/output.json 'BIDS_definitions'
    assert_file_contains ${PROJET_TMP_FOLDER}/output.json 'DatasetDescJSON'
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/output.json
}

@test 'delete files with user ${USER}' {
    rm ${PROJET_TMP_FOLDER}/db_get.json
}