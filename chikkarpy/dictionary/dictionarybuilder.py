from logging import DEBUG, StreamHandler, getLogger
from dartsclone import DoubleArray
from sortedcontainers import SortedDict
from .jtypedbytebuffer import JTypedByteBuffer
from .flags import Flags


class DictionaryBuilder:
    __BYTE_MAX_VALUE = 127

    class SynonymEntry:
        headword = None
        group_id = None
        lexeme_ids = None
        flags = None
        category = None

    @staticmethod
    def __default_logger():
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
                if (not row or row.isspace()):
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
        if len(cols) < 9:
            raise ValueError('invalid format')
        if cols[2] == "2":
            return None
        entry = self.SynonymEntry()
        entry.group_id = int(cols[0])
        entry.lexeme_ids = cols[0] if cols[3] == "" else list(
            map(int, cols[3].split("/")))
        entry.headword = cols[8]
        has_ambiguity = self.parse_boolean(cols[2], "0", "1")
        is_noun = self.parse_boolean(cols[1], "2", "1")
        form_type = self.parse_int(cols[4], 4)
        acronym_type = self.parse_int(cols[5], 2)
        variant_type = self.parse_int(cols[6], 3)
        entry.flags = Flags(has_ambiguity, is_noun, form_type, acronym_type, variant_type)
        entry.category = cols[7]
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
                self.write_shortarray(entry.lexeme_ids)
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

    def parse_boolean(self, s, false_string, true_string):
        if s == false_string:
            return False
        elif s == true_string:
            return True
        else:
            raise ValueError("invalid value: " + s)

    def parse_int(self, s, limit):
        v = int(s)
        if v < 0 or v > limit:
            raise ValueError("invalid value: " + s)
        return v

    def write_string(self, text):
        len_ = 0
        for c in text:
            if 0x10000 <= ord(c) <= 0x10FFFF:
                len_ += 2
            else:
                len_ += 1
        self.write_stringlength(len_)
        self.byte_buffer.write_str(text)

    def write_shortarray(self, array):
        self.byte_buffer.write_int(len(array), 'byte')
        for item in array:
            self.byte_buffer.write_int(item, 'short')

    def write_stringlength(self, len_):
        if len_ <= self.__BYTE_MAX_VALUE:
            self.byte_buffer.write_int(len_, 'byte')

    def __logging_size(self, size):
        self.logger.info('{} bytes\n'.format(size))

    def read_loffer_config(self):
        pass
