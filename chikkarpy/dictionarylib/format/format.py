from enum import IntEnum


class Column(IntEnum):
    """https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md"""
    GROUP_ID = 0
    IS_NOUN = 1
    AMBIGUITY = 2
    LEXEME_IDS = 3
    FORM_TYPE = 4
    ACRONYM_TYPE = 5
    VARIANT_TYPE = 6
    CATEGORY = 7
    HEAD_WORD = 8


class IsNoun(IntEnum):
    TRUE = 1
    FALSE = 2


class Ambiguity(IntEnum):
    FALSE = 0
    TRUE = 1
    INVALID = 2


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
