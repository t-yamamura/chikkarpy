import struct


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
