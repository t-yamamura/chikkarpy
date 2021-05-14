

class SynonymGroup(object):
    """
    A container of synonyms
    """
    def __init__(self, gid, synonyms):
        """Constructs a new group with the specified synonym group ID and the list of synonyms.

        Args:
            gid (int): a synonym group ID
            synonyms (list[chikkarpy.synonym.Synonym]): a list of synonyms
        """
        self.gid = gid
        self.synonyms = synonyms

    def get_id(self):
        """Returns the ID of this group.

        Returns:
            int: the ID of this group
        """
        return self.gid

    def get_synonyms(self):
        """Returns the list of synonyms in this group.

        Returns:
            list[chikkarpy.synonym.Synonym]: the list of synonyms in this group
        """
        return self.synonyms

    def lookup(self, word):
        """Returns a synonym from this group with the specified headword.

        Args:
            word (str): a headword

        Returns:
            chikkarpy.synonym.Synonym | None: the synonym with the specified headword, or None if a synonym is not found
        """
        for synonym in self.synonyms:
            if synonym.get_head_word() == word:
                return synonym

        return None
