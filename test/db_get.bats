export DATABASE_NAME=NEW_BIDS_DB

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
    cat <<EOT >> test/db_get.json 
        {
            "owner": "${USER}",
            "database": "${DATABASE_NAME}",
            "BIDS_definitions": ["Anat", "Ieeg", "DatasetDescJSON"]
        }
EOT
}


@test "can run docker db.get" {
    run docker run -it --rm \
        -v $(pwd)/test:/input \
        -v $(pwd)/test:/output \
        -v $(pwd)/scripts:/scripts \
        bids-converter  \
        --command=db.get \
        --input_data=/input/db_get.json \
        --output_file=/output/output.json      
}

@test 'assert_file_contains()' {
    assert_file_contains test/output.json 'BIDS_definitions'
    assert_file_contains test/output.json 'DatasetDescJSON'
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} test/output.json
}

@test 'delete files with user ${USER}' {
    rm test/db_get.json
    rm test/output.json
}