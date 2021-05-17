import mmap

from dartsclone import DoubleArray

from . import idtable


class DoubleArrayTrie(object):

    def __init__(self, bytes_, offset):
        """Constructs a new double-array trie

        Args:
            bytes_ (mmap.mmap): a memory-mapped dictionary
            offset (int): byte offset
        """
        position = offset
        self.trie = DoubleArray()
        bytes_.seek(position)

        # trie size
        size = int.from_bytes(bytes_.read(4), 'little')
        position += 4

        # trie array
        array = memoryview(bytes_)[position:position + size * 4]
        self.trie.set_array(array, size)
        position += self.trie.total_size()

        self.group_id_table = idtable.IdTable(bytes_, position)
        position += self.group_id_table.storage_size()

        self.storage_size = position - offset

    def lookup_by_common_prefix(self, text, offset):
        """Searches group IDs with the `text` by common prefix.

        Args:
            text (bytes): a memory-mapped dictionary
            offset (int): byte offset

        Yields:
            tuple[int, int]: a group ID and
        """
        key = text[offset:]
        result = self.trie.common_prefix_search(key, length=len(key))
        for index, length in result:
            group_ids = self.group_id_table.get(index)
            length += offset
            for group_id in group_ids:
                yield group_id, length

    def lookup_by_exact_match(self, text):
        """Searches group IDs with the ``text`` by exact match.

        Args:
            text (bytes): a head word to search for

        Returns:
            list[int]: a list of synonym group IDs
        """
        results = self.trie.exact_match_search(text)
        if results[0] < 0:
            return []
        else:
            return list(self.group_id_table.get(results[0]))

    def get_storage_size(self):
        """int: a storage size of the double-array trie"""
        return self.storage_size
