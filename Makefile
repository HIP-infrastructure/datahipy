.DEFAULT_GOAL := help

# Define the version tag for the python package
# and the docker image
TAG = $(shell python get_version.py)
# Replace + with - for docker tags
MODIFIED_TAG = $(subst +,-,$(TAG))

#test: @ Run all tests
.PHONY: test
test:
	@echo "Running pytest tests..."
	docker run -t --rm \
		--entrypoint "/entrypoint_pytest.sh" \
		-v $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/test:/test \
		-v $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/bids_tools:/apps/bids_tools/bids_tools \
		$(if $(CI_REGISTRY),$(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG),bids-tools:$(MODIFIED_TAG)) \
		${USER} \
		$(shell id -u $(USER)) \
		/test

#build: @ Builds the Docker image
build:
	docker build \
	-t $(if $(CI_REGISTRY),$(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG),bids-tools:$(MODIFIED_TAG)) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
	--build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	--build-arg VERSION=$(TAG) .

#build-release: @ Release the new Docker image with the new version tag
build-release:
	docker build \
		-t $(if $(CI_REGISTRY),$(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG),bids-tools:$(MODIFIED_TAG)) \
		--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
        --build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
        --build-arg VERSION=$(TAG) .

#python-install: @ Installs the python package
install-python:
	pip install -e .[all]

#install-python-wheel: @ Installs the python wheel
install-python-wheel: build-python-wheel
	pip install bids_tools

#python-wheel: @ Builds the python wheel
build-python-wheel:
	python setup.py sdist bdist_wheel

#test-python-install: @ Tests the python package installation
test-python-install: install-python install-python-wheel	
	bids_tools --version

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
