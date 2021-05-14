
class Chikkar(object):
    """
    A container of synonym dictionaries.
    """
    def __init__(self):
        self._dictionaries = []
        self._enable_verb = False

    def enable_verb(self):
        """Enable verb and adjective synonyms.

        After this method is called, ``self.find()`` searches for synonyms for verbs and adjectives.
        """
        self._enable_verb = True

    def add_dictionary(self, dictionary):
        """Add a synonym dictionary.

        Adds a dictionary to be used for search. When searching, the dictionary added later takes precedence.

        Args:
            dictionary (chikkarpy.dictionary.Dictionary): a synonym dictionary
        """
        self._dictionaries.insert(0, dictionary)

    def find(self, word, group_ids=None):
        """Returns synonyms for the specified word.

        If the tries in the dictionaries are enabled and ``group_ids`` is not ``None``,
        use the synonym group IDs as keys. Otherwise, use ``word`` as a key.
        If ``enable_verb`` is not called, only noun synonyms are returned.

        Args:
            word (str): keyword
            group_ids (list[int]): synonym group IDs

        Returns:
            list[str]: a list of synonyms
        """
        for dictionary in self._dictionaries:
            gids = dictionary.lookup(word, group_ids)
            if len(gids) == 0:
                continue

            synonyms = []
            for gid in gids:
                ret = self.gather_head_word(word, gid, dictionary)
                if ret:
                    synonyms += ret
            return synonyms

        return []

    def gather_head_word(self, word, gid, dictionary):
        """

        Args:
            word (str):
            gid (int):
            dictionary (chikkarpy.dictionary.Dictionary):

        Returns:
            list[str] | None: head words
        """
        head_words = []

        synonym_group = dictionary.get_synonym_group(gid)
        if synonym_group is None:
            return None

        looked_up = synonym_group.lookup(word)
        if looked_up is None:
            raise ValueError("The dictionary (``{}``) has a group ID of {}, "
                             "but the key (``{}``) dose not exist in the group.".format(dictionary.filename, gid, word))
        if looked_up.has_ambiguity():
            return None

        for synonym in synonym_group.get_synonyms():
            if synonym.get_head_word() == word:
                continue
            if not self._enable_verb and not synonym.is_noun():
                continue

            head_words.append(synonym.get_head_word())
        return head_words
