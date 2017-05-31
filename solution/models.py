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
        return self.item.itemName

    @staticmethod
    def createCommerce(obj, sellerObj):
        commerceAnalysis = obj['commerceAnalysis']
        seller = Seller.registrationSeller(obj['hostUID'], obj['hostName'], sellerObj, commerceAnalysis)
        item = Item.registrationItem(commerceAnalysis['item'], seller.category)
        commerce = Commerce.objects.create(item=item, seller=seller, content=obj['content'], title=obj['title'],
                                distance=obj['distance'], timer=obj['timer'])
        commerce.save()
        return commerce