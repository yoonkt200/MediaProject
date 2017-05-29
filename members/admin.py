from django.contrib import admin
from members.models import MemberDivision, Member, Seller, Buyer


class MemberDivisionAdmin(admin.ModelAdmin):
    model = MemberDivision
    list_display = ('divisionName', 'info')


class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ('memberName', 'is_admin', 'userId')


class SellerAdmin(admin.ModelAdmin):
    model = Seller
    list_display = ('member', 'category', 'phoneNumber')


class BuyerAdmin(admin.ModelAdmin):
    model = Buyer
    list_display = ('member', 'phoneNumber')


admin.site.register(MemberDivision, MemberDivisionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Buyer, BuyerAdmin)