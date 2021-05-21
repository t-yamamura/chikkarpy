import struct

from . import dictionaryversion
from .jtypedbytebuffer import JTypedByteBuffer


class DictionaryHeader(object):
    """
    A header of a dictionary file.
    """
    __DESCRIPTION_SIZE = 256
    __STORAGE_SIZE = 8 + 8 + __DESCRIPTION_SIZE

    def __init__(self, version, create_time, description):
        """Constructs a dictionary header.

        Args:
            version (int): a dictionary version ID
            create_time (int): dictionary creation time (unix time)
            description (str): description of a dictionary
        """
        self._version = version
        self._create_time = create_time
        self._description = description

    @classmethod
    def from_bytes(cls, bytes_, offset):
        """Reads the dictionary header from the specified byte object and returns a ``DictionaryHeader`` object.

        Args:
            bytes_ (mmap.mmap): a memory-mapped dictionary
            offset (int): byte offset

        Returns:
            DictionaryHeader: a dictionary header
        """
        version, create_time = struct.unpack_from("<2Q", bytes_, offset)
        offset += 16

        len_ = 0
        while len_ < cls.__DESCRIPTION_SIZE:
            if bytes_[offset + len_] == 0:
                break
            len_ += 1
        description = bytes_[offset:offset + len_].decode("utf-8")
        return cls(version, create_time, description)

    def storage_size(self):
        """int: a storage size of the dictionary header"""
        return self.__STORAGE_SIZE

    def to_byte(self):
        """DictionaryHeader to binary converter.

        Returns:
            bytes: a binarized dictionary header
        """
        buf = JTypedByteBuffer(b'\x00' * (16 + self.__DESCRIPTION_SIZE))
        buf.seek(0)
        buf.write_int(self.version, 'long', signed=False)
        buf.write_int(self.create_time, 'long')
        dbesc = self.description.encode('utf-8')
        if len(dbesc) > self.__DESCRIPTION_SIZE:
            raise ValueError('description is too long')
        buf.write(dbesc)
        return buf.getvalue()

    @property
    def version(self):
        """int: a dictionary version ID"""
        return self._version

    @property
    def create_time(self):
        """int: dictionary creation time (unix time)"""
        return self._create_time

    @property
    def description(self):
        """str: description of a dictionary"""
        return self._description

    def is_dictionary(self):
        """Returns ``True`` if, and only if, the file is a system dictionary.

        Returns:
            bool: ``True`` if the file is a system dictionary, otherwise ``False``
        """
        return dictionaryversion.is_dictionary(self.version)
