from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from members.models import Seller, Buyer
from solution.models import Commerce, CommerceSellRegression, PopularText
from commerce.models import Item

from apyori import apriori


# 분석 소개 메인페이지
@csrf_exempt
@login_required(login_url='/')
def MainPage(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    return render(request, 'pages/index_page.html', {'seller': seller})


# 회귀분석 모델을 이용한 설명변수 추출 솔루션
@csrf_exempt
@login_required(login_url='/')
def InfluenceAnalysis(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    commerceModel = CommerceSellRegression.getLatestModel(seller.category)
    mostInfluential = commerceModel.findMostInfluential()
    # # 변수들의 회귀계수는 xx, xx, xx으로, 가장 영향력이 높은 요소는 xx입니다.
    return render(request, 'pages/sales_effect_analysis_page.html',
                  {'model': commerceModel, 'mostValuable': mostInfluential, 'seller': seller})


# Ajax 로 예측 수치를 보내면 예측결과 리턴해줌
@csrf_exempt
def Prediction(request):
    if request.POST:
        if request.user.is_authenticated():
            seller = Seller.getSeller(request.user)
        price = int(request.POST['priceInput'])
        timer = int(request.POST['timerSelect'])*3600
        distance = int(request.POST['distanceSelect'])*1000

        commerceModel = CommerceSellRegression.getLatestModel(seller.category)
        prediction = commerceModel.predict(price, timer, distance)
        # # 예상되는 판매 전환율은 xx%입니다.
        # # 작은글씨로 -> adjusted R squared : xx (예측 모델의 적합도 수치)
        return JsonResponse({'success': 'success', 'prediction': prediction, 'adjr2': commerceModel.adjr2})


# 제휴아이템 추천 랜딩페이지
@csrf_exempt
@login_required(login_url='/')
def RecommendItemPage(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    items = Item.getItemsInCategory(seller.category)
    return render(request, 'pages/product_recommend_page.html', {'seller': seller, 'items': items})


# Ajax 로 추천받을 아이템을 입력받고, 제휴아이템 연관분석 추출 & 리턴
@csrf_exempt
def RecommendItem(request):
    if request.POST:
        if request.user.is_authenticated():
            seller = Seller.getSeller(request.user)
        item = Item.getItem(request.POST['itemSelect'])

        commerces = Commerce.getSellersCommercesWithItem(seller, item)
        buyerlist = Commerce.getBuyerIdListByCommerces(commerces)
        transactionList = Buyer.getTransactionListInBuyerList(buyerlist)

        try:
            ## 연관분석 코드
            results = list(apriori(transactionList))
            results.sort(key=lambda x: x.support, reverse=True)
            results = [rule for rule in results if rule.support >= 0.5 and len(rule.items) > 1]

            results_array = []
            for result in results:
                if item.itemName in result.items:
                    appended_items = ""
                    for iteM in list(result.items):
                        appended_items = appended_items + ", " + iteM
                    appended_items = appended_items[2:]
                    results_array.append([appended_items, result.support * 100])
            ## 연관분석 코드 끝

            return JsonResponse({'result': 'success',
                 'rule1': results_array[0][0], 'rule2': results_array[1][0], 'rule1_support': results_array[0][1],
                 'rule2_support': results_array[1][1]})
        except:
            return JsonResponse({'result': 'fail'})


# 텍스트마이닝 키워드 추출
@csrf_exempt
@login_required(login_url='/')
def KeywordAnalysis(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    return render(request, 'pages/keyword_analysis_page.html', {'seller': seller})


@csrf_exempt
@login_required(login_url='/')
def GetKeyword(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    popularTextModel = PopularText.getLatestModel(seller.category)
    titleKeyword = popularTextModel.getTitleTextList()
    contentKeyword = popularTextModel.getContentTextList()
    return JsonResponse({'result': 'success', 'titleKeyword': titleKeyword, 'contentKeyword': contentKeyword})


# 통계테이블 제공
@csrf_exempt
@login_required(login_url='/')
def DataTable(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    return render(request, 'pages/sales_history_page.html', {'seller': seller})


# 데이터 반환 함수
@csrf_exempt
@login_required(login_url='/')
def GetTableData(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    dataList = Commerce.getTableData(seller)
    return JsonResponse({'result': 'success', 'dataList': dataList})