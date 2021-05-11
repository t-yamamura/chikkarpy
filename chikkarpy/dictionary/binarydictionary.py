
import mmap

from chikkarpy.dictionary.dictionaryheader import DictionaryHeader
from chikkarpy.dictionary.dictionaryversion import is_dictionary
from chikkarpy.dictionary.doublearraytrie import DoubleArrayTrie


class BinaryDictionary(object):

    def __init__(self, bytes_, header, trie, offset):
        self._bytes = bytes_
        self._header = header
        self._trie = trie
        self.offset = offset

    @staticmethod
    def _read_dictionary(filename, access=mmap.ACCESS_READ):
        with open(filename, 'rb') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=access)
        offset = 0

        header = DictionaryHeader.from_bytes(bytes_, offset)
        offset += header.storage_size()

        if not is_dictionary(header.version):
            raise Exception('invalid dictionary version')

        trie = DoubleArrayTrie(bytes_, offset)
        offset += trie.storage_size()

        return bytes_, header, trie, offset

    @classmethod
    def from_system_dictionary(cls, filename):
        """

        :param filename:
        :return:
        :rtype: BinaryDictionary
        """
        args = cls._read_dictionary(filename)
        version = args[2].version
        if not is_dictionary(version):
            raise IOError('invalid system dictionary')
        return cls(*args)

    def close(self):
        del self._trie
        self._bytes.close()

    @property
    def bytes(self):
        """

        :return:
        :rtype: mmap.mmap
        """
        return self._bytes

    @property
    def header(self) -> DictionaryHeader:
        """

        :return:
        :rtype: DictionaryHeader
        """
        return self._header

    @property
    def trie(self):
        """

        :return:
        :rtype: DoubleArrayTrie
        """
        return self._trie

    @property
    def offset(self):
        """

        :return:
        :rtype: int
        """
        return self.offset
