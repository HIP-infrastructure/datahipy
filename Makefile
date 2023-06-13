.DEFAULT_GOAL := help

# Define the project directory
PROJECT_DIR = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Define the version tag 
TAG = $(shell python get_version.py)
$(info TAG = $(TAG))
# Replace +, /, _ with - to normalize the tag
# in case the tag includes a branch name
override TAG := $(subst +,-,$(TAG))
override TAG := $(subst /,-,$(TAG))
override TAG := $(subst _,-,$(TAG))
$(info TAG (Normalized) = $(TAG))

# Define the complete docker image tag 
IMAGE_TAG = $(if $(CI_REGISTRY),$(CI_REGISTRY)/hip/datahipy:$(TAG),datahipy:$(TAG)) 

# Define the build date and vcs reference
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VCS_REF = $(shell git rev-parse --short HEAD)

# Define the user and user id for the docker container
USER = $(shell whoami)
USER_ID = $(shell id -u $(USER))

# Force to use buildkit for building the Docker image
export DOCKER_BUILDKIT=1

#test: @ Run all tests
.PHONY: test
test:
	@echo "Running pytest tests..."
	docker run -t --rm \
		--entrypoint "/entrypoint_pytest.sh" \
		-v $(PROJECT_DIR)/test:/test \
		-v $(PROJECT_DIR)/datahipy:/apps/datahipy/datahipy \
		$(IMAGE_TAG) \
		$(USER) \
		$(USER_ID) \
		/test
	@echo "Fix path in coverage xml report..."
	sed -i -r  \
		"s|/apps/datahipy/datahipy|$(PROJECT_DIR)/datahipy|g" \
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
	docker push $(CI_REGISTRY)/hip/datahipy:$(TAG)

#rm-docker-ci: @ Remove the Docker image with TAG to the CI registry
# from https://docs.gitlab.com/ee/user/packages/container_registry/delete_container_registry_images.html#use-gitlab-cicd
rm-docker-ci:
	./reg rm -d \
		--auth-url $(CI_REGISTRY) \
		-u $(CI_REGISTRY_USER) \
		-p $(CI_REGISTRY_PASSWORD) \
		$(CI_PROJECT_PATH):$(TAG)

#python-install: @ Installs the python package
install-python:
	pip install -e .[all]

#install-python-wheel: @ Installs the python wheel
install-python-wheel: build-python-wheel
	pip install datahipy

#build-python-wheel: @ Builds the python wheel
build-python-wheel:
	python setup.py sdist bdist_wheel

#test-python-install: @ Tests the python package installation
test-python-install: install-python install-python-wheel	
	datahipy --version

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
