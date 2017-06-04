from django.db import models

from members.models import Member, Seller, Buyer
from commerce.models import Category, Item


def getBuyerUidList(buyers):
    uid_list = []
    for key, value in buyers.items():
        uid = value['buyer']
        uid_list.append(uid)

    return uid_list


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
    sendCount = models.IntegerField(default=0)
    buyCount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.item.itemName

    # commerce의 buyer list add, Buyer의 item list add
    def manageBuyers(self, firebaseManager, buyer_uidList, item):
        if not buyer_uidList:
            return False
        else:
            for uid in buyer_uidList:
                buyer = Buyer.getBuyerByKeyId(firebaseManager, uid)
                buyer.items.add(item)
                buyer.save()
                self.buyers.add(buyer)

    def getBuyPercent(self):
        percent = str((self.buyCount / self.sendCount) * 100) + "%"
        return percent

    @staticmethod
    def createCommerce(firebaseManager, obj, sellerObj, sendCount):
        commerceAnalysis = obj['commerceAnalysis']
        uid_list = getBuyerUidList(obj['buyers'])

        seller = Seller.registrationSeller(obj['hostUID'], obj['hostName'], sellerObj, commerceAnalysis)
        item = Item.registrationItem(commerceAnalysis['item'], seller.category)
        commerce = Commerce.objects.create(item=item, seller=seller, content=obj['content'], title=obj['title'],
                                distance=obj['distance'], timer=obj['timer'], sendCount=sendCount,
                                           buyCount= len(uid_list), price=obj['price'])
        commerce.manageBuyers(firebaseManager, uid_list, item)
        commerce.save()
        return commerce

    @staticmethod
    def getTableData(seller):
        commerces = Commerce.objects.filter(seller=seller)
        if commerces:
            dataList = []
            for index, commerce in enumerate(commerces):
                buyers = commerce.buyers.all()
                averageAge = Buyer.getAverageAge(buyers)
                genderRatio = Buyer.getGenderRatio(buyers)
                dataList.append([commerce.item.itemName, commerce.price, commerce.timer, commerce.distance, commerce.title,
                                 commerce.getBuyPercent(), averageAge, genderRatio])
            return dataList
        else:
            return []



# w가 가장 높은애가 영향력이 높은것, pvalue는 믿을만한 정도를 나타냄
class CommerceSellRegression(TimeStampedModel):
    category = models.ForeignKey(Category, default=1)
    bias = models.FloatField(null=True, blank=True, default=None)
    cost = models.FloatField(null=True, blank=True, default=None)
    adjr2 = models.FloatField(null=True, blank=True, default=None)
    distance_w = models.FloatField(null=True, blank=True, default=None)
    distance_pValue = models.FloatField(null=True, blank=True, default=None)
    timer_w = models.FloatField(null=True, blank=True, default=None)
    timer_pValue = models.FloatField(null=True, blank=True, default=None)
    price_w = models.FloatField(null=True, blank=True, default=None)
    price_pValue = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.category.categoryName


class PopularText(TimeStampedModel):
    category = models.ForeignKey(Category, default=1)
    contentTextWithDelimiter = models.CharField(max_length=200, default="")
    titleTextWithDelimiter = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.category.categoryName

    @staticmethod
    def createTextModel(category, content_rank, title_rank):
        contentTextWithDelimiter = ""
        for text in content_rank:
            contentTextWithDelimiter = contentTextWithDelimiter + ',' + text[0]
        contentTextWithDelimiter = contentTextWithDelimiter[1:]

        titleTextWithDelimiter = ""
        for text in title_rank:
            titleTextWithDelimiter = titleTextWithDelimiter + ',' + text[0]
        titleTextWithDelimiter = titleTextWithDelimiter[1:]

        model = PopularText.objects.create(category=category, contentTextWithDelimiter=contentTextWithDelimiter,
                                           titleTextWithDelimiter=titleTextWithDelimiter)
        model.save()