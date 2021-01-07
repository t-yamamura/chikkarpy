import struct


class IdTable(object):
    def __init__(self, bytes_, offset):
        """

        :param mmap.mmap bytes_:
        :param int offset:
        """
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')

        self.offset = offset + 4
        self._bytes_view = memoryview(bytes_)[self.offset: self.offset + self.size]

    def __del__(self):
        self._bytes_view.release()

    def storage_size(self):
        """
        :return:
        :rtype: int
        """
        return 4 + self.size

    def get(self, index):
        length = self._bytes_view[index]
        result = struct.unpack_from("<{}I".format(length), self._bytes_view, index + 1)
        return result
