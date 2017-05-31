from django.contrib import admin
from solution.models import Commerce


class CommerceAdmin(admin.ModelAdmin):
    model = Commerce
    list_display = ('item', 'seller')


admin.site.register(Commerce, CommerceAdmin)