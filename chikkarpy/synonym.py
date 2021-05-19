from .dictionarylib.flags import Flags


class Synonym(object):
    """
    A synonym
    """
    def __init__(self, head_word, lexeme_ids, flags, category):
        """Construct a new synonym with the specified parameter.

        Args:
            head_word (str): a notation string
            lexeme_ids (list[int]): IDs of lexeme in the synonym group
            flags (Flags): encoded flags
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
        """list[int]: the IDs of the lexemes that corresponds to this synonym"""
        return self._lexeme_ids

    @property
    def category(self):
        """str: the category information of this synonym"""
        return self._category

    @property
    def flags(self):
        """Flags: encoded flags"""
        return self._flags

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
        """int: the acronym type of this synonym"""
        return self._flags.acronym_type

    @property
    def variant_type(self):
        """int: the variant type of this synonym"""
        return self._flags.variant_type

