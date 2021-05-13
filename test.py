from chikkarpy import Chikkar
from chikkarpy.dictionary import Dictionary as SynDic
from sudachipy.dictionary import Dictionary
from sudachipy.tokenizer import Tokenizer


# tokenizer_obj =
chikkar = Chikkar()
dic = SynDic("system_syn.dic", True)
chikkar.add_dictionary(dic)

synonyms = chikkar.find("開店")
print(synonyms)
