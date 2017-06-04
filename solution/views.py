from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from members.models import Seller
from solution.models import Commerce, CommerceSellRegression, PopularText
from commerce.models import Item


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
    # commerceModel = CommerceSellRegression.getLatestModel(user.category)
    # mostInfluential = commerceModel.findMostInfluential()
    # # 변수들의 회귀계수는 xx, xx, xx으로, 가장 영향력이 높은 요소는 xx입니다.
    # return render(request, 'pages/notice/notice_main_ver2.html', {'model': commerceModel, 'mostValuable': mostInfluential})
    return render(request, 'pages/sales_effect_analysis_page.html', {'seller': seller})


# Ajax 로 예측 수치를 보내면 예측결과 리턴해줌
@csrf_exempt
def Prediction(request):
    if request.POST:
        if request.user.is_authenticated():
            seller = Seller.getSeller(request.user)
        price = int(request.POST['priceInput'])
        timer = int(request.POST['timerSelect'])*3600
        distance = int(request.POST['distanceSelect'])*1000

        # commerceModel = CommerceSellRegression.getLatestModel(seller.category)
        # prediction = commerceModel.predict()
        # # 예상되는 판매 전환율은 xx%입니다.
        # # 작은글씨로 -> adjusted R squared : xx (예측 모델의 적합도 수치)
        # return JsonResponse({'success': 'success', 'prediction': prediction, 'adjr2': commerceModel.adjr2})
        return JsonResponse({'result': 'success', 'result2': 'success2'})


# 제휴아이템 추천 랜딩페이지
@csrf_exempt
@login_required(login_url='/')
def RecommendItemPage(request):
    if request.user.is_authenticated():
        seller = Seller.getSeller(request.user)
    items = Item.getItemsInCategory(seller.category)
    return render(request, 'pages/product_recommend_page.html', {'seller': seller, 'items': items})


# Ajax 로, 추천받을 아이템과 몇개까지 받을건지 입력받음
@csrf_exempt
def RecommendItem(request):
    if request.POST:
        if request.user.is_authenticated():
            seller = Seller.getSeller(request.user)
        item = Item.getItem(request.POST['itemSelect'])
        print (item)
        # commerces = Commerce.getSellersCommercesWithItem(seller, item)
        # buyerlist = Commerce.getBuyerIdListByCommerces(commerces)
        # transactionList = Buyer.getTransactionListInBuyers(buyerlist)

        # 예시 : transactionList = [['불고기버거', '불새버거'], ['비누', '불고기버거', '화분'], ['불고기버거']]
        # apriori rule 분석
        # post[상위 몇개까지] 데이터 활용하여 상위 몇개까지의 연관분석 룰 결과로 내보냄
        # 지지도까지 같이 출력

        return JsonResponse({'rule1': 'success1', 'rule2': 'success2', 'rule1_support': 'success3',
                             'rule2_support': 'success4'})


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