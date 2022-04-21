export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'

    PATH=/usr/bin:/usr/local/bin:/bin:/usr/sbin:/sbin
    # Add BATS test directory to the PATH.
    PATH="$(dirname "${BATS_TEST_DIRNAME}"):$PATH"
}

@test "can build docker image" {
    run docker build $(pwd) -t bids-converter
}

@test "can create input file" {
    cat <<EOT > test/sub_delete.json 
{
    "owner": "${USER}",
    "database": "${DATABASE_NAME}",
    "subject": "carole"
}
EOT
}

@test 'assert_dir_exists()' {
    assert_dir_exists test/test_data/${DATABASE_NAME}
    assert_dir_exists test/test_data/${DATABASE_NAME}/sub-carole
}

@test "can run docker sub.delete" {
    run docker run -it --rm \
        -v $(pwd)/test:/input \
        -v $(pwd)/test/test_data:/output \
        -v $(pwd)/scripts:/scripts \
        bids-converter  \
        --command=sub.delete \
        --input_data=/input/sub_delete.json
}

# @test 'assert_dir_not_exists()' {
#     assert_dir_not_exists test/test_data/${DATABASE_NAME}/sub-carole
# }

# @test 'assert_file_not_contains()' {
#     assert_file_not_contains test/test_data/participants.tsv 'carole'
# }

@test 'delete files with user ${USER}' {
    rm test/sub_delete.json
    # rm test/test_data/sub_info.json
}