import struct


class IdTable(object):
    def __init__(self, bytes_, offset):
        """Construct a ID table of synonyms.

        Args:
            bytes_ (mmap.mmap): a memory-mapped dictionary
            offset (int): byte offset
        """
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')

        self.offset = offset + 4
        self._bytes_view = memoryview(bytes_)[self.offset: self.offset + self.size]

    def __del__(self):
        self._bytes_view.release()

    def storage_size(self):
        """int: a storage size of the ID table"""
        return 4 + self.size

    def get(self, index):
        """Reads bytes with synonym group IDs from the specified index and returns the group IDs.

        Args:
            index (int): offset

        Returns:
            tuple[int]: a list of synonym group IDs
        """
        length = self._bytes_view[index]
        result = struct.unpack_from("<{}I".format(length), self._bytes_view, index + 1)
        return result
