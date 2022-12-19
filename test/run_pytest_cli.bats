setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build -t bids-tools ${PROJECT_ROOT}
}

@test "can successfully run all tests" {
    run docker run -it --rm \
        --entrypoint "/entrypoint_pytest.sh" \
        -v "${PROJECT_ROOT}/test":/test \
        -v "${PROJECT_ROOT}/bids_tools":/apps/bids_tools/bids_tools \
        bids-tools \
        ${USER} $(id -u $USER)  \
        /test
}

@test 'delete BIDS dataset created by tests' {
    rm -r ${PROJET_TMP_FOLDER}/${DATASET_NAME}
}