

class Synonym(object):
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
        """
        Construct a new synonym with the specified parameter.

        :param str head_word: a notation string
        :param list[int] lexeme_ids: a ID of lexeme in the synonym group
        :param chikkarpy.dictionary.flags.Flags flags: encoded flags
        :param str category: category Information of the synonym
        """
        self.head_word = head_word
        self.lexeme_ids = lexeme_ids
        self.flags = flags
        self.category = category

    def get_head_word(self):
        """
        Returns the notation of this synonym.

        :return: the notation of this synonym
        :rtype: str
        """
        return self.head_word

    def has_ambiguity(self):
        """
        Returns true if and only if this synonym has ambiguity.

        :return: true if this synonym is ambiguous, false otherwise
        :bool: bool
        """
        return self.flags.has_ambiguity()

    def get_lexeme_ids(self):
        """
        Returns the IDs of the lexemes that corresponds to this synonym.

        :return: an array of the IDs of the lexemes of this synonym
        :rtype: list[int]
        """
        return self.lexeme_ids

    def is_noun(self):
        """
        Returns true if and only if this synonym is a noun;

        :return: true if this synonym is a noun, false otherwise
        :rtype: bool
        """
        return self.flags.is_noun()

    def get_form_type(self):
        """
        Returns the word form type of this synonym.

        :return: the word form type of this synonym
        :rtype: int
        """
        return self.flags.form_type()

    def get_acronym_type(self):
        """
        Returns the acronym type of this synonym.

        :return: the acronym type of this synonym
        :rtype: int
        """
        return self.flags.acronym_type()

    def get_variant_type(self):
        """
        Returns the variant type of this synonym.

        :return: the variant type of this synonym
        :rtype: int
        """
        return self.flags.variant_type()

    def get_category(self):
        """
        Returns the category information of this synonym.

        :return: the category information of this synonym
        :rtype: str
        """
        return self.category
