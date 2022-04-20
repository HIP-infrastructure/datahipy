#!/bin/sh

./test/bats/bin/bats test/db_create.bats 
./test/bats/bin/bats test/db_get.bats 
./test/bats/bin/bats test/sub_import.bats 
./test/bats/bin/bats test/sub_get.bats 
./test/bats/bin/bats test/sub_delete.bats 
