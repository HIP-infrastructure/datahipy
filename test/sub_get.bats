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
    cat <<EOT > test/sub_get.json 
{
    "owner": "${USER}",
    "database": "${DATABASE_NAME}",
    "info": { "sub": "carole", "dtype": "Anat" }
}
EOT
}


@test "can run docker sub.get" {
    run docker run -it --rm \
        -v $(pwd)/test:/input \
        -v $(pwd)/test/test_data:/output \
        -v $(pwd)/scripts:/scripts \
        bids-converter  \
        --command=sub.get \
        --input_data=/input/sub_get.json \
        --database_path=/output/ \
        --output_file=/output/sub_info.json
}

@test 'assert_dir_exists()' {
    assert_file_exists test/test_data/sub_info.json
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} test/test_data/sub_info.json
}

@test 'assert_file_contains()' {
    assert_file_contains test/test_data/sub_info.json 'carole'
    assert_file_contains test/test_data/sub_info.json 'T1w'
}

@test 'delete files with user ${USER}' {
    rm test/sub_get.json
    rm test/test_data/sub_info.json
}