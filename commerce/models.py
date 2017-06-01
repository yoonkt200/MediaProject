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

    @staticmethod
    def registrationItem(itemName, category):
        itemName = itemName.replace(" ", "")
        item = Item.checkRegistered(itemName, category)
        if item:
            return item
        else:
            return Item.createItem(itemName, category)

    @staticmethod
    def checkRegistered(itemName, category):
        try:
            item = Item.objects.get(itemName=itemName, category=category)
        except:
            item = False

        return item

    @staticmethod
    def createItem(itemName, category):
        item = Item.objects.create(itemName=itemName, category=category)
        item.save()
        return item