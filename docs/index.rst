.. DataHIPy documentation master file, created by
   sphinx-quickstart on Tue Feb 14 11:46:23 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to `DataHIPy`'s documentation!
========================================

This data management software is developed by the HIP team at the University Hospital of Lausanne (CHUV) for use within the lab, as well as for open-source software distribution.

.. image:: https://img.shields.io/github/v/release/HIP-infrastructure/datahipy
  :alt: Latest GitHub Release
.. image:: https://img.shields.io/github/release-date/HIP-infrastructure/datahipy
  :alt: GitHub Release Date
.. image:: https://zenodo.org/badge/428721094.svg
  :target: https://zenodo.org/badge/latestdoi/428721094
  :alt: Digital Object Identifier (DOI)
.. image:: https://gitlab.hbp.link/hip/datahipy/badges/master/pipeline.svg?private_token=glpat-5cJTQmAsz3as-x3xzx47
  :target: https://gitlab.hbp.link/hip/datahipy/-/commits/master
  :alt: CI/CD
.. image:: https://codecov.io/github/HIP-infrastructure/datahipy/branch/master/graph/badge.svg?token=F1CWBIGXJN 
  :target: https://codecov.io/github/HIP-infrastructure/datahipy
  :alt: Code Coverage

.. TODO add badge for maybe docs 

Introduction
-------------

`DataHIPy` is an open-source tool written in Python and encapsulated in a Docker image to handle neuroimaging data on the Human Intracranial EEG Platform (HIP) following Brain Imaging Data Structure (`BIDS <https://bids-specification.readthedocs.io>`__).

Aknowledgment
--------------

If your are using `DataHIPy` in your work, please acknowledge this software and its dependencies. See :ref:`Citing <citing>` for more details.

License information
--------------------

This software is distributed under the open-source Apache 2.0 license. See :ref:`license <LICENSE>` for more details.

All trademarks referenced herein are property of their respective holders.

Help/Questions
---------------

If you run into any problems or have any code bugs or questions, please create a new `GitHub Issue <https://github.com/HIP-infrastructure/datahipy/issues>`_.

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
   :caption: About DataHIPy

   LICENSE
   citing
   CHANGES
   contributing
