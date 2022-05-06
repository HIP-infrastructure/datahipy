#!/bin/sh

./bats/bin/bats test_db_create.bats 
./bats/bin/bats test_db_get.bats 
./bats/bin/bats test_sub_import.bats 
./bats/bin/bats test_sub_edit_clinical.bats 
./bats/bin/bats test_sub_get.bats
./bats/bin/bats test_sub_delete_file.bats 
./bats/bin/bats test_sub_delete.bats 
./bats/bin/bats test_db_cleanup.bats 
