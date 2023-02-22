from bids_tools.info import (
    __version__,
    __author__,
    __email__,
    __maintainer__,
    __credits__,
    __license__,
    __status__,
    __url__,
    __packagename__,
    __release_date__,
    __copyright__,
    __doc__,
    DOWNLOAD_URL,
    DOCKER_HUB
)

from . import _version
__version__ = _version.get_versions()['version']
