import struct

from chikkarpy.synonym import Synonym
from chikkarpy.synonymgroup import SynonymGroup
from chikkarpy.dictionary.flags import Flags


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
        :rtype: SynonymGroup
        """
        if group_id not in self.group_id_to_offset:
            return None

        offset = self.group_id_to_offset[group_id]
        self.bytes_.seek(offset)  # ? self.bytes_.seek(self.group_id_to_offset[group_id])

        synonyms = []
        n = int.from_bytes(self.bytes_.read(2), 'little')
        for i in range(n):
            head_word = self.buffer_to_string()
            lexeme_ids = self.buffer_to_short_array()
            flags = int.from_bytes(self.bytes_.read(2), 'little')
            category = self.buffer_to_string()
            synonyms.append(Synonym(head_word, lexeme_ids, Flags.from_int(flags), category))
        return SynonymGroup(group_id, synonyms)

    def buffer_to_string_length(self):
        """
        :return:
        :rtype: int
        """
        length = self.bytes_.read_byte()
        if length < 128:
            return length
        else:
            low = self.bytes_.read_byte()
            return ((length & 0x7F) << 8) | low

    def buffer_to_string(self):
        """
        :return:
        :rtype:
        """
        length = self.buffer_to_string_length()
        return self.bytes_.read(2 * length).decode('utf-16-le')

    def buffer_to_short_array(self):
        length = self.bytes_.read_byte()
        _bytes = self.bytes_.read(2 * length)
        return list(struct.unpack('{}h'.format(length), _bytes))
