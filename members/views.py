from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from members.models import Member, Seller


# 로그인 관련 함수