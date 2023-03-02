# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""This file contains bids_tools package information."""

import datetime


__version__ = "1.0.0"

__current_year__ = datetime.datetime.now().strftime("%Y")

__release_date__ = "DD.MM.{}".format(__current_year__)

__author__ = "The HIP team"

__copyright__ = (
    "Copyright (C) 2022-{}, ".format(__current_year__)
    + "the HIP team and Contributors, All rights reserved."
)

__credits__ = (
    "Contributors: please check the ``.zenodo.json`` file at the top-level folder"
    "of the repository"
)
__license__ = "Apache 2.0"
__maintainer__ = "The HIP team"
__email__ = "support@hip.ch"
__status__ = "Prototype"

__packagename__ = "bids-tools"

__url__ = "https://github.com/HIP-infrastructure/{name}/tree/{version}".format(
    name=__packagename__, version=__version__
)

DOWNLOAD_URL = (
    "https://github.com/HIP-infrastructure{name}/archive/{ver}.tar.gz".format(
        name=__packagename__, ver=__version__
    )
)

DOCKER_HUB = "TO_BE_COMPLETED_ONCE_IT_IS_DEPLOYED"
