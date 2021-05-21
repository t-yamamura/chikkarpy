import os
from logging import getLogger
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve
from zipfile import ZipFile


DEFAULT_RESOURCEDIR = Path(__file__).absolute().parent / 'resources'
DEFAULT_RESOURCEDIR = DEFAULT_RESOURCEDIR.as_posix()


DICT_VERSION = "20200722"
DICT_PREFIX = "sudachi-synonym"
BINARY_NAME = "system_synonym.dic"

ZIP_URL = (
    "https://sudachi.s3-ap-northeast-1.amazonaws.com/sudachisynonym/"
    "{}-{}.zip".format(DICT_PREFIX, DICT_VERSION)
)
ZIP_NAME = urlparse(ZIP_URL).path.split("/")[-1]
UNZIP_NAME = "{}-{}".format(DICT_PREFIX, DICT_VERSION)

logger = getLogger(__name__)


def download_dictionary():
    if not os.path.exists(DEFAULT_RESOURCEDIR):
        logger.warning("Downloading the Sudachi Synonym dictionary (It may take a while) ...")

        _, _msg = urlretrieve(ZIP_URL, ZIP_NAME)
        with ZipFile(ZIP_NAME) as z:
            z.extractall()

        os.rename(UNZIP_NAME, DEFAULT_RESOURCEDIR)
        os.remove(ZIP_NAME)

        logger.warning("... downloaded and placed the dictionary at `{}`.".format(DEFAULT_RESOURCEDIR))
    else:
        logger.warning("Resource is already installed at `{}`.".format(DEFAULT_RESOURCEDIR))


def get_system_dictionary_path():
    dictionary_path = os.path.join(DEFAULT_RESOURCEDIR, BINARY_NAME)
    if not os.path.exists(dictionary_path):
        raise FileNotFoundError("Synonym dictionary is not installed.")

    return dictionary_path
