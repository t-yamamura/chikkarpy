import time
import argparse
from chikkarpy.dictionarylib.dictionaryversion import SYSTEM_DICT_VERSION_1
from chikkarpy.dictionarylib.dictionaryheader import DictionaryHeader
from chikkarpy.dictionarylib.dictionarybuilder import DictionaryBuilder

def parse_argment():
    parser = argparse.ArgumentParser(
        description="usage: DictionaryBuilder -o file [-d description] input\n")
    parser.add_argument(dest="input_path",
                        type=str, help="the synonym_dict.txt")
    parser.add_argument("-o", dest="output_path",
                        type=str, help="the bynary synonym file")
    parser.add_argument("-d", type=str, default="", dest="description", help="description comment")
    return parser.parse_args()


def main():
    args = parse_argment()
    header = DictionaryHeader(SYSTEM_DICT_VERSION_1, int(time.time()), args.description)
    with open(args.output_path, "bw") as output:
        output.write(header.to_byte())

        builder = DictionaryBuilder()
        builder.build(args.input_path, output)

if __name__ == "__main__":
    main()