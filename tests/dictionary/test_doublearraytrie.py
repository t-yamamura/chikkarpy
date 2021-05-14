import mmap
import os

from unittest import TestCase

from chikkarpy.dictionary.dictionaryheader import DictionaryHeader
from chikkarpy.dictionary.doublearraytrie import DoubleArrayTrie


class TestDoubleArrayTrie(TestCase):

    ENCODING = "utf-8"

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'dict', 'system.dic')
        with open(dic_file, 'rb') as f:
            bytes_ = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        header = DictionaryHeader.from_bytes(bytes_, 0)
        self.trie = DoubleArrayTrie(bytes_, header.storage_size())

    def test_common_prefix_search(self):
        results = list(self.trie.lookup("open".encode(self.ENCODING), 0))
        self.assertEqual(len(results), 2)
        r1, r2 = results
        self.assertEqual(r1[0], 6)
        self.assertEqual(r1[1], 4)
        self.assertEqual(r2[0], 100006)
        self.assertEqual(r2[1], 4)

    def test_exact_match(self):
        self.assertCountEqual(self.trie.lookup_from_bytes("open".encode(self.ENCODING)), [6, 100006])
        self.assertFalse(self.trie.lookup_from_bytes("nothing".encode(self.ENCODING)))

    def test_storage_size(self):
        self.assertEqual(self.trie.get_storage_size(), 1095)
