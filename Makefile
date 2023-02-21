.DEFAULT_GOAL := help

# Define the project directory
PROJECT_DIR = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Define the version tag for the python package
# and the docker image
TAG = $(shell python get_version.py)
# Replace +, /, _ with - for docker tags
MODIFIED_TAG = $(subst +,-,$(TAG))
MODIFIED_TAG = $(subst /,-,$(MODIFED_TAG))
MODIFIED_TAG = $(subst _,-,$(MODIFED_TAG))

# Define the complete docker image tag 
IMAGE_TAG = $(if $(CI_REGISTRY),$(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG),bids-tools:$(MODIFIED_TAG)) 

# Define the build date and vcs reference
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VCS_REF = $(shell git rev-parse --short HEAD)

# Define the user and user id for the docker container
USER = $(shell whoami)
USER_ID = $(shell id -u $(USER))

#test: @ Run all tests
.PHONY: test
test:
	@echo "Running pytest tests..."
	docker run -t --rm \
		--entrypoint "/entrypoint_pytest.sh" \
		-v $(PROJECT_DIR)/test:/test \
		-v $(PROJECT_DIR)/bids_tools:/apps/bids_tools/bids_tools \
		$(IMAGE_TAG) \
		$(USER) \
		$(USER_ID) \
		/test
	@echo "Fix path in coverage xml report..."
	sed -i -r  \
		"s|/apps/bids_tools/bids_tools|$(PROJECT_DIR)/bids_tools|g" \
		$(PROJECT_DIR)/test/report/cov.xml

#build-docker: @ Builds the Docker image
build-docker:
	docker build \
	-t $(IMAGE_TAG) \
	--build-arg BUILD_DATE=$(BUILD_DATE) \
	--build-arg VCS_REF=$(VCS_REF) \
	--build-arg VERSION=$(TAG) .

#push-docker-ci: @ Push the Docker image with TAG to the CI registry
push-docker-ci:
	docker push $(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG)

#clean-docker-ci: @ Remove the Docker image from the CI registry
clean-docker-ci:
	docker rmi $(CI_REGISTRY)/hip/bids-tools:$(MODIFIED_TAG)

#python-install: @ Installs the python package
install-python:
	pip install -e .[all]

#install-python-wheel: @ Installs the python wheel
install-python-wheel: build-python-wheel
	pip install bids_tools

#build-python-wheel: @ Builds the python wheel
build-python-wheel:
	python setup.py sdist bdist_wheel

#test-python-install: @ Tests the python package installation
test-python-install: install-python install-python-wheel	
	bids_tools --version

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
