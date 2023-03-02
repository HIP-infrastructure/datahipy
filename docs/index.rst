.. bids_tools documentation master file, created by
   sphinx-quickstart on Tue Feb 14 11:46:23 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to `bids_tools`'s documentation!
========================================

This data management software is developed by the HIP team at the University Hospital of Lausanne (CHUV) for use within the lab, as well as for open-source software distribution.

.. image:: https://img.shields.io/github/v/release/HIP-infrastructure/bids-tools?include_prereleases
  :alt: Latest GitHub Release
.. image:: https://img.shields.io/github/release-date-pre/HIP-infrastructure/bids-tools
  :alt: GitHub Release Date
.. image:: https://zenodo.org/badge/428721094.svg
  :target: https://zenodo.org/badge/latestdoi/428721094
  :alt: Digital Object Identifier (DOI)
.. image:: https://gitlab.hbp.link/hip/bids-tools/badges/master/pipeline.svg
  :target: https://gitlab.hbp.link/hip/bids-tools/-/commits/master
  :alt: CI/CD
.. image:: https://gitlab.hbp.link/hip/bids-tools/badges/master/coverage.svg
  :target: https://gitlab.hbp.link/hip/bids-tools/-/commits/master
  :alt: Coverage

.. TODO add badge for maybe docs 

Introduction
-------------

`bids_tools` is an open-source tool written in Python and encapsulated in a Docker image to handle neuroimaging data on the Human Intracranial EEG Platform (HIP) following Brain Imaging Data Structure (`BIDS <https://bids-specification.readthedocs.io>`__).

Aknowledgment
--------------

If your are using `bids_tools` in your work, please acknowledge this software and its dependencies. See :ref:`Citing <citing>` for more details.

License information
--------------------

This software is distributed under the open-source Apache 2.0 license. See :ref:`license <LICENSE>` for more details.

All trademarks referenced herein are property of their respective holders.

Help/Questions
---------------

If you run into any problems or have any code bugs or questions, please create a new `GitHub Issue <https://github.com/HIP-infrastructure/bids-tools/issues>`_.

Eager to contribute?
---------------------

See :ref:`Contributing <contributing>` for more details.

Funding
--------

This project received funding from the European Union's H2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3, as part the Human Intracerebral EEG Platform (HIP)).

Contents
=========

.. _getting_started:

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   installation

.. _user-docs:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   usage

.. _developer-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   developer

.. _api-doc:

.. toctree::
   :maxdepth: 5
   :caption: API Documentation

   api_cli_module
   api_handlers_module
   api_bids_module

.. _about-docs:

.. toctree::
   :maxdepth: 1
   :caption: About bids_tools

   LICENSE
   citing
   CHANGES
   contributing
