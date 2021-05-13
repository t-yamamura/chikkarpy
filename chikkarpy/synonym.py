

class Synonym(object):
    """
    A synonym
    """

    # Typical form
    __NONE = 0

    # Translated from another language
    __FORM_TRANSLATION = 1
    # Alias or common name
    __FORM_ALIAS = 2
    # Old name
    __FORM_OLD_NAME = 3
    # Misused words
    __FORM_MISNOMER = 4

    # Abbreviations written in Latin letters
    __ACRONYM_ALPHABET = 1
    # Abbreviations written outside the Latin alphabet
    __ACRONYM_OTHERS = 2

    # Original spelling of foreign words or romanization of Japanese words
    __VARIANT_ALPHABET = 1
    # Variant notation
    __VARIANT_GENERAL = 2
    # Misspelled words
    __VARIANT_MISSPELLED = 3

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
        return self.category

    def has_ambiguity(self):
        """Returns ``True`` if and only if this synonym has ambiguity.

        Returns:
            bool: ``True`` if this synonym is ambiguous, ``False`` otherwise
        """
        return self._flags.has_ambiguity

    def is_noun(self):
        """Returns ``True`` if and only if this synonym is a noun;

        Returns:
            bool: ``True`` if this synonym is a noun, ``False`` otherwise
        """
        return self._flags.is_noun

    def form_type(self):
        """Returns the word form type of this synonym.

        Returns:
            int: the word form type of this synonym
        """
        return self._flags.form_type

    def acronym_type(self):
        """Returns the acronym type of this synonym.

        Returns:
            int: the acronym type of this synonym
        """
        return self._flags.acronym_type

    def variant_type(self):
        """Returns the variant type of this synonym.

        Returns:
            int: the variant type of this synonym
        """
        return self._flags.variant_type

