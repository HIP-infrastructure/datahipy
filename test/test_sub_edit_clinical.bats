export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_edit_clinical.json 
{
    "database": "${DATABASE_NAME}",
    "subject": "carole",
    "clinical" : {
    	"age": "30",
        "sex": "M",
        "handedness": "L",
        "hospital": "CHUGA"
    }
}
EOT
}


@test "can run docker sub.get" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        ${USER} $(id -u $USER) \
        --command=sub.edit.clinical \
        --input_data=/input/sub_get.json \
        --output_file=/output/sub_edit_clinical.json
}

@test 'assert_dir_exists()' {
    assert_file_exists ${PROJET_TMP_FOLDER}/sub_edit_clinical.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/sub_edit_clinical.json
}

@test 'assert_file_contains()' {
    assert_file_contains ${PROJET_TMP_FOLDER}/sub_edit_clinical.json 'carole'
    assert_file_contains ${PROJET_TMP_FOLDER}/sub_edit_clinical.json 'CHUGA'
}

@test 'delete files with user ${USER}' {
    rm ${PROJET_TMP_FOLDER}/sub_edit_clinical.json
}