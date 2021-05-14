from functools import singledispatch


class Flags:
    def __init__(self, has_ambiguity, is_noun, form_type, acronym_type, variant_type):
        """

        Args:
            has_ambiguity (bool): ``True`` if a synonym is ambiguous, ``False`` otherwise
            is_noun (bool): ``True`` if a synonym is a noun, ``False`` otherwise
            form_type (int):
            acronym_type (int):
            variant_type (int):
        """
        self._has_ambiguity = has_ambiguity
        self._is_noun = is_noun
        self._form_type = form_type
        self._acronym_type = acronym_type
        self._variant_type = variant_type

    @classmethod
    def from_int(cls, flags):
        """

        Args:
            flags (int):

        Returns:

        """
        has_ambiguity = ((flags & 0x0001) == 1)
        is_noun = ((flags & 0x0002) == 2)
        form_type = (flags >> 2) & 0x0007
        acronym_type = (flags >> 5) & 0x0003
        variant_type = (flags >> 7) & 0x0003
        return cls(has_ambiguity, is_noun, form_type, acronym_type, variant_type)

    @property
    def has_ambiguity(self):
        return self._has_ambiguity

    @property
    def is_noun(self):
        return self._is_noun

    @property
    def form_type(self):
        return self._form_type

    @property
    def acronym_type(self):
        return self._acronym_type

    @property
    def variant_type(self):
        return self._variant_type

    def encode(self):
        """

        Returns:
            int:
        """
        flags = 0
        flags |= 1 if self.has_ambiguity else 0
        flags |= (1 if self.is_noun else 0) << 1
        flags |= self.form_type << 2
        flags |= self.acronym_type << 5
        flags |= self.variant_type << 7
        return flags
