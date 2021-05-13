
import mmap

from .dictionaryheader import DictionaryHeader
from .dictionaryversion import is_dictionary
from .doublearraytrie import DoubleArrayTrie


class BinaryDictionary(object):

    def __init__(self, bytes_, header, trie, offset):
        """

        Args:
            bytes_ (mmap.mmap):
            header (DictionaryHeader):
            trie (DoubleArrayTrie):
            offset (int):
        """
        self._bytes = bytes_
        self._header = header
        self._trie = trie
        self._offset = offset

    @staticmethod
    def _read_dictionary(filename, access=mmap.ACCESS_READ):
        """

        Args:
            filename (str):
            access (int):

        Returns:

        """
        with open(filename, 'rb') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=access)
        offset = 0

        header = DictionaryHeader.from_bytes(bytes_, offset)
        offset += header.storage_size()

        if not is_dictionary(header.version):
            raise Exception('invalid dictionary version')

        trie = DoubleArrayTrie(bytes_, offset)
        offset += trie.get_storage_size()

        return bytes_, header, trie, offset

    @classmethod
    def from_system_dictionary(cls, filename):
        """

        Args:
            filename (str):

        Returns:
            chikkarpy.dictionary.binarydictionary.BinaryDictionary:
        """
        args = cls._read_dictionary(filename)
        if not args[1].is_dictionary():
            raise IOError('invalid system dictionary')
        return cls(*args)

    def close(self):
        del self._trie
        self._bytes.close()

    @property
    def bytes(self):
        """mmap.mmap:"""
        return self._bytes

    @property
    def header(self):
        """chikkarpy.dictionary.dictionaryheader.DictionaryHeader: a"""
        return self._header

    @property
    def trie(self):
        """chikkarpy.dictionary.doublearraytrie.DoubleArrayTrie: a"""
        return self._trie

    @property
    def offset(self):
        """int: """
        return self._offset
