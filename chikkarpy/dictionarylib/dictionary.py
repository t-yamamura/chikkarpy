from chikkarpy.synonymgroup import SynonymGroup
from .binarydictionary import BinaryDictionary
from .synonym_group_list import SynonymGroupList


class Dictionary(object):
    """
    A container of synonyms
    """
    def __init__(self, filename, enable_trie):
        """Reads the synonym dictionary from the specified file.

        If ``enableTrie`` is ``false``, a search by synonym group IDs takes precedence over a search by the headword.

        Args:
            filename (str): path of synonym dictionary file
            enable_trie (bool): true to enable trie, otherwise false
        """
        self.filename = filename
        self.dict_ = BinaryDictionary.from_system_dictionary(filename)
        self.enable_trie = enable_trie
        self.group_list = SynonymGroupList(self.dict_.bytes, self.dict_.offset)

    def lookup(self, word, group_ids):
        """Returns a synonym group ID that contains the specified headword or a specified synonym group ID.

        Args:
            word (str): a headword to search for
            group_ids (list[int] | None): an array of synonym group IDs to search for

        Returns:
            list[int]: an array of synonym group IDs found, or an empty array if not found
        """
        if self.enable_trie or group_ids is None:
            return self.dict_.trie.lookup_by_exact_match(word.encode('utf-8'))
        else:
            return group_ids

    def get_synonym_group(self, group_id):
        """Returns a group of synonyms with the specified ID.

        Args:
            group_id (int): a synonym group ID

        Returns:
            SynonymGroup | None: the group of synonyms with the specified ID, or None if no ID matches
        """
        return self.group_list.get_synonym_group(group_id)

    def close(self):
        self.dict_.close()
