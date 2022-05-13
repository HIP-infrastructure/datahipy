export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_delete.json 
{
    "database": "${DATABASE_NAME}",
    "subject": "carole"
}
EOT
}

@test 'assert_dir_exists()' {
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
}

@test "can run docker sub.delete" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}/${DATABASE_NAME}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        --command=sub.delete \
        --input_data=/input/sub_delete.json
}

@test 'assert_dir_not_exists()' {
    assert_dir_not_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
}

# TODO
# @test 'assert_file_not_contains()' {
#     assert_file_contains ${PROJET_TMP_FOLDER}/participants.tsv 'carole'
# }

@test 'delete files with user ${USER}' {
    rm ${PROJET_TMP_FOLDER}/sub_delete.json
}