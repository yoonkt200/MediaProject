from collections import Counter

from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint

from solution.models import PopularText, Commerce
from commerce.models import Category


categorys = Category.objects.all()
for index, category in enumerate(categorys):
    title_list = list(Commerce.objects.filter(category=category).values_list('title', flat=True))
    content_list = list(Commerce.objects.filter(category=category).values_list('content', flat=True))

    pos = []
    for idx, mystr in enumerate(title_list):
        row = Hannanum().nouns(mystr)
        for noun in row:
            pos.append(noun)

    cnt = Counter(pos)
    title_result = cnt.most_common(3)
    pprint(title_result)

    pos = []
    for idx, mystr in enumerate(content_list):
        row = Hannanum().nouns(mystr)
        for noun in row:
            pos.append(noun)

    cnt = Counter(pos)
    content_result = cnt.most_common(3)
    pprint(content_result)


# from collections import Counter
#
# from konlpy.tag import Hannanum
# from konlpy.utils import concordance, pprint
#
# import pandas as pd
#
# df = pd.read_csv("/Users/yoon/Documents/data/prev_count_data.csv")
# data = df['marketing_text'][10:50]
#
# pos = []
# for idx, mystr in enumerate(data):
#     row = Hannanum().nouns(mystr)
#     for noun in row:
#         pos.append(noun)
#
# cnt = Counter(pos)
# pprint(cnt.most_common(5))