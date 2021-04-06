from functools import singledispatch

class Flags:
    def __init__(self, has_ambiguity, is_noun, form_type, acronym_type, variant_type):
        self.has_ambiguity = has_ambiguity
        self.is_noun = is_noun
        self.form_type = form_type
        self.acronym_type = acronym_type
        self.variant_type = variant_type

    def get_Flags(self, flags):
        self.has_ambiguity = ((flags & 0x0001) == 1)
        self.is_noun = ((flags & 0x0002) == 2)
        self.form_type = (flags >> 2) & 0x0007
        self.acronym_type = (flags >> 5) & 0x0003
        self.variant_type = (flags >> 7) & 0x0003

    def get_has_ambiguity(self):
        return self.has_ambiguity

    def get_is_noun(self):
        return self.is_noun

    def get_form_type(self):
        return self.form_type

    def get_acronym_type(self):
        return self.acronym_type

    def get_variant_type(self):
        return self.variant_type

    def encode(self):
        flags = 0
        flags |= 1 if self.has_ambiguity else 0
        flags |= (1 if self.is_noun else 0) << 1
        flags |= self.form_type << 2
        flags |= self.acronym_type << 5
        flags |= self.variant_type << 7
        return flags
