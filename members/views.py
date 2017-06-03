from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from members.models import Member, Seller


# 로그인 관련 함수
@csrf_exempt
def Login(request):
    try:
        userId = request.POST['userId']
        password = request.POST['password']
        member = authenticate(userId=userId, password=password)
        if member is not None:
            if member.memberDivision.divisionName == "seller":
                login(request, member)
                seller = Seller.objects.get(member=member)
                return JsonResponse(
                    {'result': 'success', 'name': seller.member.memberName, 'category': seller.category.categoryName})
            else:
                return JsonResponse({'result': 'fail'})
        else:
            return JsonResponse({'result': 'fail'})
    except:
        return JsonResponse({'result': 'fail'})