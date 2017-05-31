from collections import Counter

from konlpy.corpus import kolaw
from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint

import pandas as pd


df = pd.read_csv("/Users/yoon/Documents/data/prev_count_data.csv")

data = df['marketing_text'][10:50]

pos = []
for idx, mystr in enumerate(data):
    row = Hannanum().nouns(mystr)
    for noun in row:
        pos.append(noun)

cnt = Counter(pos)
pprint(cnt.most_common(5))