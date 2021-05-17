from enum import IntEnum
from logging import DEBUG, StreamHandler, getLogger

from dartsclone import DoubleArray
from sortedcontainers import SortedDict

from chikkarpy.synonym import IsNoun, Ambiguity, Form, Acronym, Variant, Synonym
from .flags import Flags
from .jtypedbytebuffer import JTypedByteBuffer


class DictionaryBuilder:
    __BYTE_MAX_VALUE = 127

    class Column(IntEnum):
        """https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md"""
        GROUP_ID = 0
        IS_NOUN = 1
        AMBIGUITY = 2
        LEXEME_IDS = 3
        FORM_TYPE = 4
        ACRONYM_TYPE = 5
        VARIANT_TYPE = 6
        CATEGORY = 7
        HEAD_WORD = 8

    class SynonymWithGroupId:
        def __init__(self, group_id, synonym):
            """Constructs a synonym with its group ID

            Args:
                group_id (int): a group ID
                synonym (Synonym): a synonym object
            """
            self._synonym = synonym
            self._group_id = group_id

        @property
        def group_id(self): return self._group_id
        @property
        def headword(self): return self._synonym.head_word
        @property
        def lexeme_ids(self): return self._synonym.lexeme_ids
        @property
        def flags(self): return self._synonym.flags
        @property
        def category(self): return self._synonym.category

    @staticmethod
    def __default_logger():
        """Sets and returns a default logging

        Returns:
            StreamHandler: a default logging
        """
        handler = StreamHandler()
        handler.terminator = ""
        handler.setLevel(DEBUG)
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    def __init__(self, *, logger=None):
        self.byte_buffer = JTypedByteBuffer()
        self.trie_keys = SortedDict()
        self.synonym_groups = []
        self.is_dictionary = False
        self.logger = logger or self.__default_logger()

    def build(self, input_path, out_stream):
        with open(input_path, 'r', encoding='utf-8') as rf:
            self.build_synonym(rf)
        self.write_trie(out_stream)
        self.write_synonym_groups(out_stream)

    def build_synonym(self, synonym_input_stream):
        block = []
        line_no = -1
        group_id = -1
        try:
            for i, row in enumerate(synonym_input_stream):
                line_no = i
                if not row or row.isspace():
                    if len(block) == 0:
                        continue
                    else:
                        self.synonym_groups.append(block)
                        block = []
                        group_id = -1
                else:
                    entry = self.parse_line(row)
                    if not entry:
                        continue
                    if group_id < 0:
                        group_id = entry.group_id
                    elif group_id != entry.group_id:
                        raise ValueError("group ID is changed in block")
                    self.add_to_trie(entry.headword, group_id)
                    block.append(entry)
            if len(block) > 0:
                self.synonym_groups.append(block)
        except Exception as e:
            if line_no > 0:
                self.logger.error(
                    '{} at line {} in {}\n'.format(e.args[0], line_no, synonym_input_stream.name))
            print(row)
            raise e

    def parse_line(self, line):
        cols = line.split(",")
        if len(cols) <= max(map(int, self.Column)):
            raise ValueError('invalid format')
        if int(cols[self.Column.AMBIGUITY]) == Ambiguity.INVALID:
            return None

        group_id = int(cols[self.Column.GROUP_ID])

        lexeme_ids = cols[self.Column.GROUP_ID] if cols[self.Column.LEXEME_IDS] == "" else list(map(int, cols[self.Column.LEXEME_IDS].split("/")))
        headword = cols[self.Column.HEAD_WORD]
        _is_noun = self.parse_boolean(cols[self.Column.IS_NOUN], IsNoun.FALSE, IsNoun.TRUE)
        _has_ambiguity = self.parse_boolean(cols[self.Column.AMBIGUITY], Ambiguity.FALSE, Ambiguity.TRUE)
        _form_type = self.parse_int(cols[self.Column.FORM_TYPE], max(map(int, Form)))
        _acronym_type = self.parse_int(cols[self.Column.ACRONYM_TYPE], max(map(int, Acronym)))
        _variant_type = self.parse_int(cols[self.Column.VARIANT_TYPE], max(map(int, Variant)))
        flags = Flags(_has_ambiguity, _is_noun, _form_type, _acronym_type, _variant_type)
        category = cols[self.Column.CATEGORY]

        entry = self.SynonymWithGroupId(group_id, Synonym(headword, lexeme_ids, flags, category))

        return entry

    def add_to_trie(self, headword, group_id):
        key = headword.encode('utf-8')
        if key not in self.trie_keys:
            self.trie_keys[key] = []
        self.trie_keys[key].append(group_id)

    def write_trie(self, io_out):
        trie = DoubleArray()
        keys = []
        vals = []
        id_table = JTypedByteBuffer()
        for key, ids in self.trie_keys.items():
            keys.append(key)
            vals.append(id_table.tell())
            id_table.write_int(len(ids), 'byte')
            for _id in ids:
                id_table.write_int(_id, 'int')
        self.logger.info('building the trie...')
        trie.build(keys, lengths=[len(k) for k in keys], values=vals)
        self.logger.info('done\n')
        self.logger.info('writing the trie...')
        self.byte_buffer.clear()
        self.byte_buffer.write_int(trie.size(), 'int')
        self.byte_buffer.seek(0)
        io_out.write(self.byte_buffer.read())
        self.byte_buffer.clear()
        io_out.write(trie.array())
        self.__logging_size(trie.size() * 4 + 4)
        trie.clear()
        del trie

        self.logger.info('writing the word-ID table...')
        self.byte_buffer.write_int(id_table.tell(), 'int')
        self.byte_buffer.seek(0)
        io_out.write(self.byte_buffer.read())
        self.byte_buffer.clear()
        id_table.seek(0)
        io_out.write(id_table.read())
        self.__logging_size(id_table.tell() + 4)
        del id_table

    def write_synonym_groups(self, io_out):
        mark = io_out.tell()
        io_out.seek(mark + 4 * len(self.synonym_groups) * 2 + 4)
        offsets = JTypedByteBuffer()
        offsets.write_int(len(self.synonym_groups), 'int')
        self.logger.info('writing the word_infos...')
        base = io_out.tell()
        for entries in self.synonym_groups:
            if len(entries) == 0:
                continue
            offsets.write_int(entries[0].group_id, 'int')
            offsets.write_int(io_out.tell(), 'int')

            self.byte_buffer.write_int(len(entries), 'short')
            for entry in entries:
                self.write_string(entry.headword)
                self.write_short_array(entry.lexeme_ids)
                self.byte_buffer.write_int(entry.flags.encode(), 'short')
                self.write_string(entry.category)
            self.byte_buffer.seek(0)
            io_out.write(self.byte_buffer.read())
            self.byte_buffer.clear()

        self.__logging_size(io_out.tell() - base)
        self.logger.info('writing synonym groups offsets...')
        io_out.seek(mark)
        offsets.seek(0)
        io_out.write(offsets.read())
        self.__logging_size(offsets.tell())

    @staticmethod
    def parse_boolean(s, false_value, true_value):
        v = int(s)
        if v == false_value:
            return False
        elif v == true_value:
            return True
        else:
            raise ValueError("invalid value: {}".format(s))

    @staticmethod
    def parse_int(s, limit):
        v = int(s)
        if v < 0 or v > limit:
            raise ValueError("invalid value: {}".format(s))
        return v

    def write_string(self, text):
        len_ = 0
        for c in text:
            if 0x10000 <= ord(c) <= 0x10FFFF:
                len_ += 2
            else:
                len_ += 1
        self.write_string_length(len_)
        self.byte_buffer.write_str(text)

    def write_short_array(self, array):
        self.byte_buffer.write_int(len(array), 'byte')
        for item in array:
            self.byte_buffer.write_int(item, 'short')

    def write_string_length(self, len_):
        if len_ <= self.__BYTE_MAX_VALUE:
            self.byte_buffer.write_int(len_, 'byte')
        else:
            self.byte_buffer.write_int((len_ >> 8) | 0x80, 'byte')
            self.byte_buffer.write_int((len_ & 0xFF), 'byte')

    def __logging_size(self, size):
        self.logger.info('{} bytes\n'.format(size))
