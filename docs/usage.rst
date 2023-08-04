.. _cmdusage:

***********************
Commandline Usage
***********************

Commandline Arguments
=============================

The command to run the main `DataHIPy` commandline interface is as follows.

.. argparse::
		:ref: datahipy.cli.run.get_parser
		:prog: datahipy

Commands
--------

Here is a list of all the commands available in the ``--command`` argument of the `datahipy` commandline interface with an example of input JSON file (``--input_data`` argument) generated and used by the ``test/cli/test_run.py`` script for testing each command.

.. tip::

    The tests in ``test/cli/test_run.py`` can also provide a good support for understanding the usage of each command.

Dataset
~~~~~~~

``dataset.create``
^^^^^^^^^^^^^^^^^^

Create a version tag in a Datalad-controlled BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/create_dataset.json
        :code: json

``dataset.create_tag``
^^^^^^^^^^^^^^^^^^^^^^

Create a version tag in a Datalad-controlled BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/dataset_create_tag.json
        :code: json

``dataset.get_tags``
^^^^^^^^^^^^^^^^^^^^^

Get the list of existing version tags for a Datalad-controlled BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/dataset_get_tags.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/dataset_get_tags_output.json
        :code: json

``dataset.checkout_tag``
^^^^^^^^^^^^^^^^^^^^^^^^

Checkout a Datalad-controlled BIDS dataset at a specific tag, the master branch, or the HEAD.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/dataset_checkout_tag.json
        :code: json

``dataset.release_version``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make a patch (``1.0.0`` → ``1.0.1``) / minor (``1.0.0`` → ``1.1.0``) / major (``1.1.0`` → ``2.0.0``) version release of a Datalad-controlled BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/dataset_release_version.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/dataset_release_version_output.json
        :code: json

``dataset.get``
^^^^^^^^^^^^^^^

Get a JSON summary of dataset consisting of all fields, participants, and existing entities.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/get_dataset.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/get_dataset_output.json
        :code: json

``datasets.get``
^^^^^^^^^^^^^^^^^

Get a list of JSON summaries of all datasets.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/get_datasets.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/get_datasets_output.json
        :code: json

Participant
~~~~~~~~~~~

``sub.import``
^^^^^^^^^^^^^^

Import and update files for a given participant into an existing BIDS dataset. An appropriate record is added/updated to the ``participants.tsv`` tabular file if needed.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/import_sub.json
        :code: json

``sub.get``
^^^^^^^^^^^

Get information about data available for a given participant of a dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/get_sub.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/get_sub_output.json
        :code: json

``sub.edit.clinical``
^^^^^^^^^^^^^^^^^^^^^

Edit the participant’s information stored in the ``participants.tsv`` tabular file.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/sub_edit_clinical.json
        :code: json

``sub.delete``
^^^^^^^^^^^^^^

Remove a participant from a given BIDS dataset. The record will be deleted from the ``participants.tsv`` tabular file.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/delete_sub.json
        :code: json

``sub.delete.file``
^^^^^^^^^^^^^^^^^^^

Remove data file(s) from a BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/delete_sub_file.json
        :code: json

Project
~~~~~~~

``project.create``
^^^^^^^^^^^^^^^^^^

Create a new Datalad-controlled project dataset in the collaborative space of the HIP.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/create_project.json
        :code: json

``project.sub.import``
^^^^^^^^^^^^^^^^^^^^^^

Import an existing `sub-<participant_label>` folder from a BIDS dataset of the center space of the HIP to the BIDS dataset of the project (located in ``<project_directory>/inputs/bids-dataset``).

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/import_project_sub.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/import_project_sub_output.json
        :code: json

``project.doc.import``
^^^^^^^^^^^^^^^^^^^^^^

Import an existing document from the center space of the HIP to the `documents/` folder of the project.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/import_project_doc.json
        :code: json

``project.create_tag``
^^^^^^^^^^^^^^^^^^^^^^

Create a version tag in a Datalad-controlled project dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/project_create_tag.json
        :code: json

``project.get_tags``
^^^^^^^^^^^^^^^^^^^^

Get the list of existing version tags for a Datalad-controlled project dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/project_get_tags.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/project_get_tags_output.json
        :code: json

``project.checkout_tag``
^^^^^^^^^^^^^^^^^^^^^^^^

Checkout a Datalad-controlled project dataset at a specific tag, the master branch, or the HEAD.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/project_checkout_tag.json
        :code: json

``project.release_version``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make a patch (``1.0.0`` → ``1.0.1``) / minor (``1.0.0`` → ``1.1.0``) / major (``1.1.0`` → ``2.0.0``) version release of a Datalad-controlled project dataset and its nested BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/project_release_version.json
        :code: json

Example of content of output JSON data:

    .. include:: examples/io/project_release_version_output.json
        :code: json

.. _cmdusage-docker:

Running `DataHIPy` in Docker
================================

Please have a look at the special REST API service of the HIP Gateway! This service creates and executes the different commands of `DataHIPy` in Docker. The source code is available at the following URL: 

    https://github.com/HIP-infrastructure/gateway/blob/master/src/tools/tools.service.ts
