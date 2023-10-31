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

   or ::

    pip install -e .\[all\]

.. _instructions_docs_build:

How to build the documentation locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `DataHIPy` and its dependencies (see :ref:`instructions_datahipy_install`).

2. Go to the `docs` of the cloned repository and build the HTML documentation with `make`::

    cd docs
    make clean && make html

   The built HTML files of the documentation, including its main page (``index.html``), can be found in the ``docs/build/html`` directory, and can be opened in your favorite browser.

.. note::
	If you have made any changes in the `DataHIPy` docstrings, make sure to re-install `DataHIPy` prior to building the documentation by running ``pip install -e .[all]`` / ``pip install -e .\[all\]``.

.. _instructions_tests:

How to run the tests via the Docker image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to the clone directory of your fork and (re-)build the Docker image with the following commands ::

    cd DataHIPy
    make -B build-docker

2. Run the tests throughout the Docker image ::

    make test

.. _instructions_tests_local:

How to run the tests locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. (Re-)Install `DataHIPy` and its dependencies (see :ref:`instructions_datahipy_install`).

2. Run the `pytest` tests with the script provided in the repository as follow::

    sh test/run_tests.sh

.. _tests_outputs:

Outputs of tests
~~~~~~~~~~~~~~~~~

In both cases, the tests are run in a temporary `tmp` directory in the `test` directory, so that the original data are not modified. After completion, coverage report in HTML format can be found in ``test/report/cov_html`` and be displayed by opening ``index.html`` in your favorite browser.
