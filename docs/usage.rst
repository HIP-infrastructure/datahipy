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

``dataset.get``
^^^^^^^^^^^^^^^

Get a JSON summary of dataset consisting of all fields, participants, and existing entities.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/get_dataset.json
        :code: json

``dataset.create``
^^^^^^^^^^^^^^^^^^

Create a new BIDS dataset.

Example of content of input JSON data for the ``--input_data`` argument when using this command:

    .. include:: examples/io/create_dataset.json
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

.. _cmdusage-docker:

Running `DataHIPy` in Docker
================================

TBC
