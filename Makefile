.DEFAULT_GOAL := help


#test: @ Run all tests
.PHONY: test
test:
	git submodule update --recursive
	cd test && ./run_tests.sh

#build: @ Builds the project
build: 
	docker build . -t bids-tools
	docker tag bids-tools:latest bids-converter:latest

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

