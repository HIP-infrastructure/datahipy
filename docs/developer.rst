.. _instructions:

***************************
Instructions for Developers
***************************

.. _instructions_docker_build:

How to build the Docker image locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to the clone directory of your fork and run the following command in the terminal ::

    cd DataHIPy
    make -B build-docker

.. note::
    The tag of the version of the image is generated from the git tag thanks to the versioneer.py library.

.. _instructions_datahipy_install:

How to install `DataHIPy` locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::
    `DataHIPy` requires a Python environment with `python>=3.8`.

1. Install `bids_manager` dependencies::

    pip install \
        PyQt5==5.15.4 \
        xlrd \
        PySimpleGUI \
        pydicom \
        paramiko \
        tkcalendar \
        bids_validator

2. Install `DataHIPy` along with all dependencies (including dependencies to build the documentation and to test the package)::

    pip install -e .[all]

.. _instructions_docs_build:

How to build the documentation locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `DataHIPy` and its dependencies (see :ref:`instructions_datahipy_install`).

2. Go to the `docs` of the cloned repository and build the HTML documentation with `make`::

    cd docs
    make html

.. note::
	If you have made any changes in the docstrings, make sure to have run ``pip install -e .[all]`` prior to building the documentation.

.. _instructions_tests:

How to run the tests via the Docker image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Run the Docker image with the following command::

    docker run -it --rm \
        --entrypoint "/entrypoint_pytest.sh" \
        -v "${PROJECT_ROOT}/test":/test \
        -v "${PROJECT_ROOT}/datahipy":/apps/datahipy/datahipy \
        datahipy:<version> \
        ${USER} \
        $(id -u $USER) \
        /test
    
    where:
    - `${PROJECT_ROOT}` is the path to the root of the cloned repository.
    - `<version>` is the version of the Docker image (see :ref:`instructions_docker_build`).

.. note::
    The tests are run in a temporary `tmp` directory in the `test` directory, so that the original data are not modified. After completion, coverage report in HTML format can be found in ``test/report/cov_html`` and be displayed by opening ``index.html`` in your favorite browser.


How to run the tests locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `DataHIPy` and its dependencies (see :ref:`instructions_datahipy_install`).

2. Run the `pytest` tests with the script provided in the repository as follow::

    sh test/run_tests.sh

.. note::
    The tests are run in a temporary `tmp` directory in the `test` directory, so that the original data are not modified. After completion, coverage report in HTML format can be found in ``test/report/cov_html`` and be displayed by opening ``index.html`` in your favorite browser.


