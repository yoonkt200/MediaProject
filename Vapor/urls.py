"""Vapor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from fbconnector.views import Linker
from solution.views import MainPage, InfluenceAnalysis, Prediction, RecommendItemPage, RecommendItem, KeywordAnalysis, DataTable
from members.views import Login, Logout


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^backgounrd$', Linker),

    url(r'^$', TemplateView.as_view(template_name="pages/index_login_page.html")),
    url(r'^login', Login),
    url(r'^logout', Logout),

    url(r'^main$', MainPage),
    url(r'^analysis_influence$', InfluenceAnalysis),
    url(r'^analysis_influence_prediction$', Prediction),
    url(r'^recommend_item$', RecommendItemPage),
    url(r'^recommend_item_rules$', RecommendItem),
    url(r'^analysis_keyword$', KeywordAnalysis),
    url(r'^sales_history$', DataTable),
]
