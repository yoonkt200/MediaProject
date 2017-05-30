from django.db import models

from members.models import Member, Seller, Buyer
from commerce.models import Category, Item


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Commerce(TimeStampedModel):
    item = models.ForeignKey(Item, default=1)
    seller = models.ForeignKey(Seller, default=1)
    buyers = models.ManyToManyField('members.Buyer')
    content = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200, default="")
    distance = models.IntegerField(default=0)
    timer = models.IntegerField(default=0)

    def __str__(self):
        return self.item

    @staticmethod
    def createCommerce(obj, sellerObj):
        obj['distance']
        obj['content']
        obj['timer']
        obj['title']
        commerceAnalysis = obj['commerceAnalysis']
        seller = Seller.registrationSeller(obj['hostUID'], obj['hostName'], sellerObj, commerceAnalysis)
        item = Item.registrationItem(commerceAnalysis['item'], seller.category)

        return False