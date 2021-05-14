from enum import IntEnum


class Form(IntEnum):
    # Typical form
    NONE = 0
    # Translated from another language
    TRANSLATION = 1
    # Alias or common name
    ALIAS = 2
    # Old name
    OLD_NAME = 3
    # Misused words
    MISNOMER = 4


class Acronym(IntEnum):
    # Typical Abbreviations
    NONE = 0
    # Abbreviations written in Latin letters
    ALPHABET = 1
    # Abbreviations written outside the Latin alphabet
    OTHERS = 2


class Variant(IntEnum):
    # Typical form
    NONE = 0
    # Original spelling of foreign words or romanization of Japanese words
    ALPHABET = 1
    # Variant notation
    GENERAL = 2
    # Misspelled words
    MISSPELLED = 3


class Synonym(object):
    """
    A synonym
    """
    def __init__(self, head_word, lexeme_ids, flags, category):
        """Construct a new synonym with the specified parameter.

        Args:
            head_word (str): a notation string
            lexeme_ids (list[int]): a ID of lexeme in the synonym group
            flags (chikkarpy.dictionary.flags.Flags): encoded flags
            category (str): category Information of the synonym
        """
        self._head_word = head_word
        self._lexeme_ids = lexeme_ids
        self._flags = flags
        self._category = category

    @property
    def head_word(self):
        """str: the notation of this synonym"""
        return self._head_word

    @property
    def lexeme_ids(self):
        """list[int]: the IDs of the lexemes that corresponds to this synonym."""
        return self._lexeme_ids

    @property
    def category(self):
        """str: the category information of this synonym"""
        return self._category

    @property
    def has_ambiguity(self):
        """bool: ``True`` if this synonym is ambiguous, ``False`` otherwise"""
        return self._flags.has_ambiguity

    @property
    def is_noun(self):
        """bool: ``True`` if this synonym is a noun, ``False`` otherwise"""
        return self._flags.is_noun

    @property
    def form_type(self):
        """int: the word form type of this synonym"""
        return self._flags.form_type

    @property
    def acronym_type(self):
        """int: the acronym type of this synonym."""
        return self._flags.acronym_type

    @property
    def variant_type(self):
        """int: the variant type of this synonym."""
        return self._flags.variant_type

