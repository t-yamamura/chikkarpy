from unittest import TestCase

from chikkarpy.dictionarylib.format import Form, Acronym, Variant
from chikkarpy.dictionarylib.flags import Flags


class TestFlags(TestCase):

    def test_all_zero(self):
        flags = Flags(False, False, Form.NONE, Form.NONE, Form.NONE)
        code = flags.encode()
        new_flags = Flags.from_int(code)
        self.assertFalse(new_flags.has_ambiguity)
        self.assertFalse(new_flags.is_noun)
        self.assertEqual(new_flags.form_type, Form.NONE)
        self.assertEqual(new_flags.acronym_type, Form.NONE)
        self.assertEqual(new_flags.variant_type, Form.NONE)

    def test_max(self):
        flags = Flags(True, True, Form.MISNOMER, Acronym.OTHERS, Variant.MISSPELLED)
        code = flags.encode()
        new_flags = Flags.from_int(code)
        self.assertTrue(new_flags.has_ambiguity)
        self.assertTrue(new_flags.is_noun)
        self.assertEqual(new_flags.form_type, Form.MISNOMER)
        self.assertEqual(new_flags.acronym_type, Acronym.OTHERS)
        self.assertEqual(new_flags.variant_type, Variant.MISSPELLED)
