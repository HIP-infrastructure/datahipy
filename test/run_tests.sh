#!/bin/sh

# Get the directory of this script (e.g. datahipy/test)
TESTDIR=$(cd "$(dirname "$0")"; pwd)
# Go to this directory (if script is called from another directory)
cd $TESTDIR

# Run the tests
./bats/bin/bats test_dataset_cleanup.bats
./bats/bin/bats run_pytest_cli.bats
