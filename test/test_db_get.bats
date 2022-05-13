export DATABASE_NAME=NEW_BIDS_DB

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/db_get.json 
        {
            "user": "${USER}",
            "userId": $(id -u $USER),
            "database": "${DATABASE_NAME}",
            "BIDS_definitions": ["Anat", "Ieeg", "DatasetDescJSON"]
        }
EOT
}


@test "can run docker db.get" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        --command=db.get \
        --input_data=/input/db_get.json \
        --output_file=/output/output.json      
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