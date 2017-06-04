from django.shortcuts import render
from django.http import JsonResponse

from collections import Counter

from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint

from solution.models import PopularText, Commerce
from commerce.models import Category


# 텍스트마이닝 키워드 추출
def TextMining_batch(request):
    categorys = Category.objects.all()
    for index, category in enumerate(categorys):
        title_list = list(Commerce.objects.filter(item__category=category).values_list('title', flat=True))
        content_list = list(Commerce.objects.filter(item__category=category).values_list('content', flat=True))

        if title_list and content_list:
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

            PopularText.createTextModel(category, content_result, title_result)

    return JsonResponse({'result': 'success'})