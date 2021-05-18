import mmap
import os

from unittest import TestCase

from chikkarpy.dictionarylib.dictionaryheader import DictionaryHeader
from chikkarpy.dictionarylib.dictionaryversion import SYSTEM_DICT_VERSION_1


class TestDictionaryHeader(TestCase):

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources', 'system.dic')
        with open(dic_file, 'rb') as f:
            bytes_ = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.header = DictionaryHeader.from_bytes(bytes_, 0)

    def test_version(self):
        self.assertTrue(self.header.version, SYSTEM_DICT_VERSION_1)

    def test_create_time(self):
        self.assertTrue(self.header.create_time > 0)

    def test_description(self):
        self.assertEqual(self.header.description, "the system dictionary for the unit tests")

    def test_is_dictionary(self):
        self.assertTrue(self.header.is_dictionary())