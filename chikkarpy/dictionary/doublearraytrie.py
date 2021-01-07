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
        position += 4

        # trie array
        array = memoryview(bytes_)[position:position + size * 4]
        self.trie.set_array(array, size)
        position += self.trie.total_size()

        self.group_id_table = idtable.IdTable(bytes_, position)
        position += self.group_id_table.storage_size()

        self.storage_size = position - offset

    def storage_size(self):
        """
        :return:
        :rtype: int
        """
        return self.storage_size
