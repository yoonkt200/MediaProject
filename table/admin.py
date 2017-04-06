from django.contrib import admin
from table.models import Test


class TestAdmin(admin.ModelAdmin):
    model = Test
    list_display = ('testfield',)


admin.site.register(Test, TestAdmin)
