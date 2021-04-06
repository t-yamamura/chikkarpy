class Flags(object):
    def __init__(self, has_ambiguity, is_noun, form_type, acronym_type, variant_type):
        """

        :param bool has_ambiguity:
        :param bool is_noun:
        :param int form_type:
        :param int acronym_type:
        :param int variant_type:
        """
        self._has_ambiguity = has_ambiguity
        self._is_noun = is_noun
        self._form_type = form_type
        self._acronym_type = acronym_type
        self._variant_type = variant_type

    def has_ambiguity(self):
        """

        :return:
        :rtype: bool
        """
        return self._has_ambiguity

    def is_noun(self):
        """

        :return:
        :rtype: bool
        """
        return self._is_noun

    def form_type(self):
        """

        :return:
        :rtype: int
        """
        return self._form_type

    def acronym_type(self):
        """

        :return:
        :rtype: int
        """
        return self._acronym_type

    def variant_type(self):
        """

        :return:
        :rtype: int
        """
        return self._variant_type

    def encode(self):
        pass