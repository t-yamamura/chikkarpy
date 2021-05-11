

from .binarydictionary import BinaryDictionary
from .synonym_group_list import SynonymGroupList


class Dictionary(object):
    """
    A container of synonyms
    """

    def __init__(self, filename, enable_trie):
        """

        :param str filename: path of synonym dictionary file
        :param bool enable_trie: true to enable trie, otherwise false
        """
        self.dict_ = BinaryDictionary.from_system_dictionary(filename)
        self.enable_trie = enable_trie
        self.group_list = SynonymGroupList(self.dict_.bytes, self.dict_.offset)

    def lookup(self, word, group_ids):
        """
        Returns a synonym group ID that contains the specified headword or a specified synonym group ID.

        :param str word: a headword to search for
        :param list[int] group_ids: an array of synonym group IDs to search for
        :return: an array of synonym group IDs found, or an empty array if not found
        :rtype: list[int]
        """
        if self.enable_trie or group_ids is None:
            return self.dict_.trie.lookup_from_bytes(word.encode('utf-8'))
        else:
            return group_ids

    def get_synonym_group(self, group_id):
        """
        Returns a group of synonyms with the specified ID.

        :param int group_id: a synonym group ID
        :return: an Optional describing the group of synonyms with the specified ID, or an empty Optional
        """
        return self.group_list.get_synonym_group(group_id)
