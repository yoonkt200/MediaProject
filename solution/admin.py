from django.contrib import admin
from solution.models import Commerce, CommerceSellRegression, PopularText


class CommerceAdmin(admin.ModelAdmin):
    model = Commerce
    list_display = ('item', 'seller')


class CommerceSellRegressionAdmin(admin.ModelAdmin):
    model = CommerceSellRegression
    list_display = ('category', 'adjr2')


class PopularTextAdmin(admin.ModelAdmin):
    model = PopularText
    list_display = ('category', 'contentTextWithDelimiter')


admin.site.register(Commerce, CommerceAdmin)
admin.site.register(CommerceSellRegression, CommerceSellRegressionAdmin)
admin.site.register(PopularText, PopularTextAdmin)