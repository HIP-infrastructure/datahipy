export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'

    PATH=/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin
    # Add BATS test directory to the PATH.
    PATH="$(dirname "${BATS_TEST_DIRNAME}"):$PATH"
}

@test "Teardown all BIDS data left" {
    echo ${BATS_TEST_DIRNAME}
    P=test/test_data/${DATABASE_NAME}
    sudo rm -rf ${P}/derivatives \
        ${P}/sourcedata \
        ${P}/participants.tsv
}

@test "Teardown BIDS_IMPORT" {
    echo ${BATS_TEST_DIRNAME}
    sudo rm -rf test/test_data/BIDS_IMPORT
}

