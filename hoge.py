from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary as SynDic
from sudachipy.dictionary import Dictionary
from sudachipy.tokenizer import Tokenizer


# tokenizer_obj =
chikkar = Chikkar()

system_dic = SynDic("system_syn.dic", False)
chikkar.add_dictionary(system_dic)
print(chikkar.find("粗筋"))
print(chikkar.find("nothing", group_ids=[6]))

# system_dic = SynDic("tests/dict/system.dic", False)
# user_dic = SynDic("tests/dict/user.dic", True)
# user2_dic = SynDic("tests/dict/user2.dic", True)
#
# chikkar.add_dictionary(system_dic)
# chikkar.add_dictionary(user2_dic)
# chikkar.add_dictionary(user_dic)
# synonyms = chikkar.find("nothing", group_ids=[5])
# print(synonyms)
