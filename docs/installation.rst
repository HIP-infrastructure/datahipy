.. _installation:

***********************************
Installation Instructions for Users
***********************************


Prerequisites
==============

Installation and use of the `DataHIPy` and dependencies have been facilitated through the use of `Docker <https://www.docker.com/>`_ software containerization. If you adopt this approach, which is recommended, you need to have Docker engine installed (see instructions in :ref:`manual-install-docker`).

While Docker enables `DataHIPy` to be run on all major operating systems where you have root privileges. A Docker image can be easily converted to a Singularity image to run `DataHIPy` on Linux systems where you might not have root privileges such as a High Performance Computing cluster (See `examples <https://docs.sylabs.io/guides/3.7/user-guide/cli/singularity_pull.html#examples>`_).

Please check https://docs.docker.com/get-started/overview/ if you want to learn more about Docker.

.. note::
    If you do not want to use Docker, `DataHIPy` can also be installed locally (see :ref:`instructions_datahipy_install`).


.. _manual-install-docker:

Installation of Docker Engine
------------------------------

* Install Docker Engine corresponding to your system:

  * For Ubuntu, follow the instructions from https://docs.docker.com/install/linux/docker-ce/ubuntu/

  * For Mac OSX (>=10.10.3), get the .dmg installer from https://store.docker.com/editions/community/docker-ce-desktop-mac

  * For Windows (>=10), get the installer from https://store.docker.com/editions/community/docker-ce-desktop-windows

* Set Docker to be managed as a non-root user

  * Open a terminal

  * Create the docker group::

    $ sudo groupadd docker

  * Add the current user to the docker group::

    $ sudo usermod -G docker -a $USER

  * Reboot

    After reboot, test if docker is managed as non-root::

      $ docker run hello-world


.. _manual-build-docker-image:

Building the Docker Image
=========================

The Docker image can be built from the Makefile provided in the `DataHIPy` repository as follows:

.. code-block:: bash

    $ # Clone locally the datahipy repository
    $ git clone https://github.com/HIP-infrastructure/DataHIPy.git DataHIPy
    $ # Go to the DataHIPy directory
    $ cd DataHIPy
    $ # Build the docker image
    $ make -B build-docker

You can then inspect the Docker image version tag with the following command:

.. code-block:: bash

    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    datahipy          <version>           0e0b0b0b0b0b        1 minute ago        2.94GB

Once you know the image tag, you can test the built image by running the command which returns the version installed in the Docker image as follows:

.. code-block:: bash

    $ docker run -it --rm \
        datahipy:<version> \
        ${USER} \
        $(id -u $USER) \
        --version

We refer to :ref:`cmdusage-docker` for more details on how to run the Docker image.
