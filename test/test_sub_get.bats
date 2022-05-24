setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_get.json 
{
    "sub": "carole"
}
EOT
}


@test "can run docker sub.get" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}/${DATABASE_NAME}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        ${USER} $(id -u $USER) \
        --command=sub.get \
        --input_data=/input/sub_get.json \
        --output_file=/input/sub_info.json
}

@test 'assert_dir_exists()' {
    assert_file_exists ${PROJET_TMP_FOLDER}/sub_get.json
    assert_file_exists ${PROJET_TMP_FOLDER}/sub_info.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/sub_info.json
}

@test 'assert_file_contains()' {
    assert_file_contains ${PROJET_TMP_FOLDER}/sub_info.json 'carole'
    assert_file_contains ${PROJET_TMP_FOLDER}/sub_info.json 'T1w'
}

@test 'delete files with user ${USER}' {
    #rm ${PROJET_TMP_FOLDER}/sub_get.json
}