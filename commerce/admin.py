from django.contrib import admin
from commerce.models import CategoryDivision, Category, Item


class CategoryDivisionAdmin(admin.ModelAdmin):
    model = CategoryDivision
    list_display = ('divisionCode', 'divisionName')


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('categoryDivision', 'categoryCode', 'categoryName')


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('category', 'itemName')


admin.site.register(CategoryDivision, CategoryDivisionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)