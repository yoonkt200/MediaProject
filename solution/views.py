from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from solution.models import Commerce, CommerceSellRegression, PopularText
from commerce.models import CategoryDivision, Category, Item


# @csrf_exempt
# def InfluenceAnalysis(request):
#     commerceModel = CommerceSellRegression.getLatestModel(user.category)
#     mostInfluential = commerceModel.findMostInfluential()
#     # 변수들의 회귀계수는 xx, xx, xx으로, 가장 영향력이 높은 요소는 xx입니다.
#     return render(request, 'pages/notice/notice_main_ver2.html', {'model': commerceModel, 'mostValuable': mostInfluential})
#
#
# # Ajax 로 예측 수치를 보내면 예측결과 리턴해줌
# @csrf_exempt
# def Prediction(request):
#     commerceModel = CommerceSellRegression.getLatestModel(user.category)
#     prediction = commerceModel.predict()
#     # 예상되는 판매 전환율은 xx%입니다.
#     # 작은글씨로 -> adjusted R squared : xx(예측 모델의 적합도)
#     return JsonResponse({'success': 'success', 'prediction': prediction, 'adjr2': commerceModel.adjr2})
#
#
