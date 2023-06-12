#!/usr/bin/env bats

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image with Makefile" {
    run bash -c "cd ${PROJECT_ROOT} && make -B build" 
}

@test "can successfully run all tests" {
    run docker run -it --rm \
        --entrypoint "/entrypoint_pytest.sh" \
        -v "${PROJECT_ROOT}/test":/test \
        -v "${PROJECT_ROOT}/datahipy":/apps/datahipy/datahipy \
        bids-tools \
        ${USER} $(id -u $USER)  \
        /test
}

@test 'delete BIDS dataset created by tests' {
    rm -r ${PROJET_TMP_FOLDER}/${DATASET_NAME}
}