# chikkarpy
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/release/python-350/)
![Build Status](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)

chikkarpyは[chikkar](https://github.com/WorksApplications/chikkar)のPython版です。 
chikkarpy is a Python version of chikkar.

chikkarpy は [Sudachi 同義語辞書](https://github.com/WorksApplications/SudachiDict/)を利用し、[SudachiPy](https://github.com/WorksApplications/SudachiPy)の出力に同義語展開を追加するために開発されたライブラリです。

単体でも同義語辞書の検索ツールとして利用できます。

## 利用方法 Ussage
## TL;DR
```
$ pip install chikkarpy

$ echo "閉店" | chikkarpy
クローズ,close,店仕舞い 000005

$ echo "金" | chikkarpy
お金,マネー,money,カネ  000020
金色,黄金色,ゴールド,gold,黄金  013372
```

## Step 1. chikkarpyのインストール
```
$ pip install chikkarpy
```

## Step 2. 使用方法
### コマンドライン
```
$ echo "金" | chikkarpy
お金,マネー,money,カネ  000020
金色,黄金色,ゴールド,gold,黄金  013372
```
chikkarpyは入力された単語を見て一致する同義語のリストを返します。
複数の同義語グループがある場合は行で区別されます。
出力は`同義語リスト\t同義語グループID`の形式です。

### python ライブラリ
使用例
```
from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary

chikkar = Chikkar()

system_dic = Dictionary("system.dic", False)
chikkar.add_dictionary(system_dic)

print(chikkar.find("閉店"))
# => ['クローズ', 'close', '店仕舞い']

print(chikkar.find("閉店", group_ids=[5])) #グループIDによるフィルタリング
# => ['クローズ', 'close', '店仕舞い']
```


## 辞書の作成 Build a dictionary

新しく辞書を追加する場合は、利用前にバイナリ形式辞書の作成が必要です。
Before using new dictionary, you need to create a binary format dictionary.

```
$ chikkarpy build -o system.dic synonym_dict.csv
```
