import os
import shutil

from glob import glob
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
    logger.warning("Downloading the Sudachi Synonym dictionary (It may take a while) ...")
    # os.makedirs(DEFAULT_RESOURCEDIR, exist_ok=True)
    _, _msg = urlretrieve(ZIP_URL, ZIP_NAME)
    with ZipFile(ZIP_NAME) as z:
        z.extractall()
    os.rename(UNZIP_NAME, DEFAULT_RESOURCEDIR)

    os.remove(ZIP_NAME)

    logger.warning("... downloaded and placed the dictionary at `{}`.".format(DEFAULT_RESOURCEDIR))
