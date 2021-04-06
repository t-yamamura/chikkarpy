
class Chikkar(object):
    """
    A container of synonym dictionaries.
    """
    def __init__(self):
        self.dictionaries = []
        self.enable_verb = False

    def enable_verb(self):
        """
        Enable verb and adjective synonyms.

        :return:
        """
        self.enable_verb = True

    def add_dictionary(self, dictionary):
        """
        Add a synonym dictionary.
        Adds a dictionary to be used for search. When searching, the dictionary added later takes precedence.

        :param chikkarpy.dictionary.dictionary.Dictionary dictionary: a synonym dictionary
        :return:
        """
        self.dictionaries.append(dictionary)

    def find(self, word, group_ids=None):
        """
        Returns synonyms for the specified word.

        :param str word: keyword
        :param list[int] group_ids: synonym group IDs
        :return: a list of synonyms
        """

        for dictionary in self.dictionaries:
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

        :param str word:
        :param int gid:
        :param chikkarpy.dictionary.dictionary.Dictionary dictionary:
        :return:
        """
        synonyms = dictionary.get_synonym_group(gid)
