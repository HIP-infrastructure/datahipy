#!/usr/bin/env bash

_common_setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'

    export DATABASE_NAME=NEW BIDS_DB
    
    # get the containing directory of this file
    # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
    # as those will point to the bats executable's location or the preprocessed file respectively
    PROJECT_ROOT="$( cd "$( dirname "$BATS_TEST_FILENAME" )/.." >/dev/null 2>&1 && pwd )"
    export PROJET_TEST_FOLDER=$PROJECT_ROOT/test
    export PROJET_TMP_FOLDER=$PROJET_TEST_FOLDER/tmp

    mkdir -p $PROJET_TEST_FOLDER/tmp
    # make executables in src/ visible to PATH
    PATH="$PROJECT_ROOT/src:$PATH"
}