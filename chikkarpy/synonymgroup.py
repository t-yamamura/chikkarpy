

class SynonymGroup(object):
    """
    A container of synonyms
    """
    def __init__(self, gid, synonyms):
        """
        Constructs a new group with the specified synonym group ID and the list of synonyms.

        :param int gid: synonym group ID
        :param list[chikkarpy.synonym.Synonym] synonyms: a list of synonyms
        """
        self.gid = gid
        self.synonyms = synonyms

    def get_id(self):
        """
        Returns the ID of this group.

        :return: the ID of this group
        :rtype: int
        """
        return self.gid

    def get_synonyms(self):
        """
        Returns the list of synonyms in this group.

        :return: the list of synonyms in this group
        :rtype: list[chikkarpy.synonym.Synonym]
        """
        return self.synonyms

    def lookup(self, word):
        """
        Returns a synonym from this group with the specified headword.

        :param str word: a headword
        :return: an Optional describing the synonym with the specified headword, or an empty Optional if a synonym is not found
        :rtype:
        """
        for synonym in self.synonyms:
            if synonym.get_head_word() == word:
                return synonym

        return None
