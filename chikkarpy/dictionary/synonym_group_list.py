

class SynonymGroupList(object):

    def __init__(self, bytes_, offset):
        """

        :param mmap.mmap bytes_:
        :param int offset:
        """
        self.bytes_ = bytes_
        orig_pos = self.bytes_.tell()
        self.bytes_.seek(offset)
        self.size = int.from_bytes(self.bytes_.read(4), 'little', signed=True)  # buf.getInt();

        self.group_id_to_offset = {}
        for i in range(self.size):
            group_id = int.from_bytes(self.bytes_.read(4), 'little', signed=True)
            offset = int.from_bytes(self.bytes_.read(4), 'little', signed=True)
            self.group_id_to_offset[group_id] = offset

    def get_synonym_group(self, group_id):
        """

        :param int group_id:
        :return:
        """
        if group_id not in self.group_id_to_offset:
            return

        offset = self.group_id_to_offset[group_id]
        self.bytes_.seek(offset)  # ? self.bytes_.seek(self.group_id_to_offset[group_id])

        synonyms = []
        n = int.from_bytes(self.bytes_.read(2), 'little')


    def buffer_to_string_length(self, buffer):
        raise NotImplementedError()

    def buffer_to_string(self, buffer):
        raise NotImplementedError()

    def buffer_to_short_array(self, buffer):
        raise NotImplementedError()
