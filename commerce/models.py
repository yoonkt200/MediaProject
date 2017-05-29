from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryDivision(TimeStampedModel):
    divisionCode = models.CharField(max_length=200, default="")
    divisionName = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.divisionName


class Category(TimeStampedModel):
    categoryDivision = models.ForeignKey(CategoryDivision, default=1)
    categoryCode = models.CharField(max_length=200, default="")
    categoryName = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.categoryName


class Item(TimeStampedModel):
    category = models.ForeignKey(Category, default=1)
    itemName = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.itemName

    # @staticmethod
    # def registrationItem(itemName):
    #     itemName = itemName.replace(" ", "")
    #     item = Item.checkRegistered(itemName)
    #     if Item.checkRegistered(itemName) == True:
    #
    #     else:
    #