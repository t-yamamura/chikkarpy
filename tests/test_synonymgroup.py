from unittest import TestCase

from chikkarpy.synonym import Synonym
from chikkarpy.synonymgroup import SynonymGroup
from chikkarpy.dictionary.flags import Flags


class TestSynonymGroup(TestCase):

    def setUp(self):
        flags = Flags(False, True, 0, 0, 0)
        self.synonym_a = Synonym("aaa", [1], flags, "")
        self.synonym_b = Synonym("bbb", [2], flags, "")
        self.group = SynonymGroup(1, [self.synonym_a, self.synonym_b])

    def test_get_id(self):
        self.assertEqual(self.group.get_id(), 1)

    def test_get_synonyms(self):
        synonyms = self.group.get_synonyms()
        self.assertEqual(len(synonyms), 2)

        s = synonyms[0]
        self.assertEqual(s.get_head_word(), "aaa")
        self.assertFalse(s.has_ambiguity())
        self.assertTrue(s.is_noun())
        self.assertListEqual(s.get_lexeme_ids(), [1])
        self.assertEqual(s.get_form_type(), 0)
        self.assertEqual(s.get_acronym_type(), 0)
        self.assertEqual(s.get_variant_type(), 0)
        s = synonyms[1]
        self.assertEqual(s.get_head_word(), "bbb")

    def test_lookup(self):
        s = self.group.lookup("aaa")
        self.assertIsNotNone(s)
        self.assertEqual(s.get_head_word(), "aaa")
        s = self.group.lookup("ccc")
        self.assertIsNone(s)
