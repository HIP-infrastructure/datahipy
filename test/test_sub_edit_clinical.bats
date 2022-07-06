setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-tools
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_edit_clinical.json 
{
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


@test "can run docker sub.edit.clinical" {
    run docker run -it  \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}/${DATABASE_NAME}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-tools  \
        ${USER} $(id -u $USER) \
        --command=sub.edit.clinical \
        --input_data=/input/sub_edit_clinical.json \
        --output_file=/output/participants.tsv
}

@test 'assert_dir_exists()' {
    assert_file_exists ${PROJET_TMP_FOLDER}/sub_edit_clinical.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv
}

@test 'assert_file_contains()' {
    assert_file_contains ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv 'carole'
    assert_file_contains ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv 'handedness'
    assert_file_contains ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv 'CHUGA'
}

@test 'delete files with user ${USER}' {
    rm ${PROJET_TMP_FOLDER}/sub_edit_clinical.json
}