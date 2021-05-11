import mmap

from dartsclone import DoubleArray

from . import idtable


class DoubleArrayTrie(object):

    def __init__(self, bytes_, offset):
        """
        :param mmap.mmap bytes_:
        :param int offset:
        """
        position = offset
        self.trie = DoubleArray()
        bytes_.seek(position)

        # trie size
        size = int.from_bytes(bytes_.read(4), 'little')
        print("size", size)
        position += 4

        # trie array
        array = memoryview(bytes_)[position:position + size * 4]
        self.trie.set_array(array, size)
        position += self.trie.total_size()

        self.group_id_table = idtable.IdTable(bytes_, position)
        position += self.group_id_table.storage_size()

        self.storage_size = position - offset

    def lookup(self, text, offset):
        """

        :param bytes text:
        :param int offset:
        :return:
        """
        key = text[offset:]
        result = self.trie.common_prefix_search(key, length=len(key))
        for index, length in result:
            word_ids = self.group_id_table.get(index)
            length += offset
            for word_id in word_ids:
                yield word_id, length

    def lookup_from_bytes(self, text):
        """
        :param bytes text:
        """
        results = self.trie.exact_match_search(text)
        print(results, results[0])
        if results[0] < 0:
            return []
        else:
            return self.group_id_table.get(results[0])

    def get_storage_size(self):
        """
        :return:
        :rtype: int
        """
        return self.storage_size
