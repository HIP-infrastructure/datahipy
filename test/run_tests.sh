#!/bin/sh

./bats/bin/bats test_db_create.bats 
./bats/bin/bats test_db_get.bats 
# ./bats/bin/bats sub_import.bats 
# ./bats/bin/bats sub_get.bats
# ./bats/bin/bats sub_delete_file.bats 
# ./bats/bin/bats sub_delete.bats 
./bats/bin/bats test_db_cleanup.bats 


