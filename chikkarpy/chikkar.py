
class Chikkar(object):
    """
    A container of synonym dictionaries.
    """
    def __init__(self):
        self.dictionaries = []
        self._enable_verb = False

    def enable_verb(self):
        """
        Enable verb and adjective synonyms.

        :return:
        """
        self._enable_verb = True

    def add_dictionary(self, dictionary):
        """
        Add a synonym dictionary.
        Adds a dictionary to be used for search. When searching, the dictionary added later takes precedence.

        :param chikkarpy.dictionary.dictionary.Dictionary dictionary: a synonym dictionary
        """
        self.dictionaries.append(dictionary)

    def find(self, word, group_ids=None):
        """
        Returns synonyms for the specified word.

        :param str word: keyword
        :param list[int] group_ids: synonym group IDs
        :return: a list of synonyms
        :rtype: list[str]
        """

        for dictionary in self.dictionaries:
            gids = dictionary.lookup(word, group_ids)
            print("gids", type(gids), gids, flush=True)
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

        :param str word:
        :param int gid:
        :param chikkarpy.dictionary.dictionary.Dictionary dictionary:
        :return: head words
        :rtype: list[str] or None
        """
        head_words = []

        synonym_group = dictionary.get_synonym_group(gid)
        print("synonym_group", synonym_group)
        if synonym_group is None:
            return None

        looked_up = synonym_group.lookup(word)
        if looked_up is None:
            raise ValueError()
        if looked_up.has_ambiguity():
            return None

        for synonym in synonym_group.get_synonyms():
            if synonym.get_head_word() == word:
                continue
            if not self.enable_verb and not synonym.is_noun():
                continue

            head_words.append(synonym.get_head_word())
        return head_words
