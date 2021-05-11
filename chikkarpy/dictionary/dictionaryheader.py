import struct

from .jtypedbytebuffer import JTypedByteBuffer
from . import dictionaryversion


class DictionaryHeader(object):
    __DESCRIPTION_SIZE = 256
    __STORAGE_SIZE = 8 + 8 + __DESCRIPTION_SIZE

    def __init__(self, version, create_time, description):
        """

        :param int version: version id (16959298134372991084 == 0xeb5b87cc8b3f406c)
        :param int create_time: epoch second (1609941157)
        :param str description:
        """
        self.version = version
        self.create_time = create_time
        self.description = description

    @classmethod
    def from_bytes(cls, bytes_, offset):
        """

        :param mmap.mmap bytes_:
        :param int offset:
        :return:
        :rtype: DictionaryHeader
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
        """

        :return:
        :rtype: int
        """
        return self.__STORAGE_SIZE

    def to_byte(self):
        """

        :retrun:
        :rtype: bytes

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

    def get_create_time(self):
        """

        :return:
        :rtype: int
        """
        return self.create_time

    def get_description(self):
        """

        :return:
        :rtype: str
        """
        return self.description

    def is_dictionary(self):
        """

        :return:
        :rtype: bool
        """
        return dictionaryversion.is_dictionary(self.version)
