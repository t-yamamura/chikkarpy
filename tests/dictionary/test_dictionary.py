import os

from unittest import TestCase

from chikkarpy.dictionary import Dictionary


class TestDictionary(TestCase):

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources', 'system.dic')
        self.dict = Dictionary(dic_file, True)
        self.dict_gid = Dictionary(dic_file, False)

    def tearDown(self):
        self.dict.dict_.close()
        self.dict_gid.dict_.close()

    def test_lookup(self):
        self.assertCountEqual(self.dict.lookup("open", group_ids=None), [6, 100006])
        self.assertCountEqual(self.dict.lookup("open", group_ids=[4]), [6, 100006])

        self.assertCountEqual(self.dict_gid.lookup("open", group_ids=None), [6, 100006])
        self.assertCountEqual(self.dict_gid.lookup("open", group_ids=[4]), [4])

    def test_get_synonyms(self):
        synonym_group = self.dict.get_synonym_group(6)
        self.assertTrue(synonym_group)
        self.assertEqual(synonym_group.get_id(), 6)

        # non-existent group id in the dictionary
        synonym_group = self.dict.get_synonym_group(200)
        self.assertFalse(synonym_group)
