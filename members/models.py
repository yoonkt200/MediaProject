from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models import Q
from django.contrib.auth import authenticate, login
import datetime

from commerce.models import CategoryDivision, Category, Item


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def getBirthdayDate(str):
    if str[:1] == "1":
        return '20' + str[:2] + '-' + str[2:4] + '-' + str[4:6]
    elif str[:1] == "0":
        return '20' + str[:2] + '-' + str[2:4] + '-' + str[4:6]
    else:
        return '19' + str[:2] + '-' + str[2:4] + '-' + str[4:6]


class MemberDivision(TimeStampedModel):
    divisionName = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.divisionName


class MemberManager(BaseUserManager):

    def create_user(self, userId, memberName, memberKeyId, password=None):
        if not userId:
            raise ValueError('Users must have an ID')

        user = self.model(userId=userId, memberName=memberName, memberKeyId=memberKeyId)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, memberName, password):
        user = self.create_user(userId=userId, password=password, memberName=memberName)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(TimeStampedModel, AbstractBaseUser):
    memberDivision = models.ForeignKey(MemberDivision, default=1)
    memberName = models.CharField(max_length=200, default="")
    userId = models.CharField(max_length=200, default="", unique=True)
    objects = MemberManager()
    is_admin = models.BooleanField(default=False)
    memberKeyId = models.CharField(max_length=200, default="")
    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['memberName']

    class Meta:
        ordering = ['memberName']

    def get_full_name(self):
        return self.userId

    def get_short_name(self):
        return self.userId

    def __str__(self):
        return self.memberName

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @staticmethod
    def getMember(email, memberKeyId):
        try:
            member = Member.objects.get(Q(userId=email) | Q(memberKeyId=memberKeyId))
        except:
            member = None

        return member


class Seller(TimeStampedModel):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, )
    birthday = models.DateField(default=datetime.date.today)
    email = models.EmailField(verbose_name='email address', max_length=200)
    fcm = models.CharField(blank=True, max_length=200)
    gender = models.CharField(max_length=200, default="male")
    phoneNumber = models.CharField(blank=True, max_length=200)
    company = models.CharField(blank=True, default="", max_length=200)
    category = models.ForeignKey(Category, default=1)

    def __str__(self):
        return self.member.memberName

    @staticmethod
    def registrationSeller(memberKeyId, company, memberObj, commerceAnalysis):
        try:
            seller = Seller.objects.get(member__memberKeyId=memberKeyId)
        except:
            seller = None

        if seller is None:
            newSeller = Seller.createSeller(memberKeyId, company, memberObj, commerceAnalysis['category'])
            return newSeller
        else:
            return seller


    @staticmethod
    def createSeller(memberKeyId, company, memberObj, categoryCode):
        member = Member.getMember(memberObj['email'], memberKeyId)

        if member:
            category = Category.objects.get(categoryCode=categoryCode)
            newSeller = Seller.objects.create(member=member, birthday=getBirthdayDate(memberObj['birthday']),
                                              email=memberObj['email'], fcm=memberObj['fcm'],
                                              phoneNumber=memberObj['tel'],
                                              gender=memberObj['gender'], company=company, category=category)
            newSeller.save()
            return newSeller
        else:
            seller = Member.objects.create_user(memberObj['email'], memberObj['name'], memberKeyId=memberKeyId)
            seller.set_password(memberObj['tel'])
            seller.save()
            category = Category.objects.get(categoryCode=categoryCode)
            newSeller = Seller.objects.create(member=seller, birthday=getBirthdayDate(memberObj['birthday']),
                                              email=memberObj['email'], fcm=memberObj['fcm'],
                                              phoneNumber=memberObj['tel'],
                                              gender=memberObj['gender'], company=company, category=category)
            newSeller.save()
            return newSeller

    @staticmethod
    def getSeller(member):
        return Seller.objects.get(member=member)


class Buyer(TimeStampedModel):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, )
    birthday = models.DateField(default=datetime.date.today)
    email = models.EmailField(verbose_name='email address', max_length=200)
    fcm = models.CharField(blank=True, max_length=200)
    gender = models.CharField(max_length=200, default="male")
    phoneNumber = models.CharField(blank=True, max_length=200)
    items = models.ManyToManyField('commerce.Item')

    class Meta:
        ordering = ['member']

    def __str__(self):
        return self.member.memberName

    def getAge(self):
        age = datetime.date.today().year - self.birthday.year + 1
        return age

    @staticmethod
    def getBuyerByKeyId(firebaseManager, keyId):
        try:
            buyer = Buyer.objects.get(member__memberKeyId=keyId)
        except:
            buyer = None

        if buyer is None:
            newBuyer = Buyer.createBuyer(firebaseManager, keyId)
            return newBuyer
        else:
            return buyer

    @staticmethod
    def createBuyer(firebaseManager, keyId):
        memberObj = firebaseManager.get('/users', keyId)
        member = Member.getMember(memberObj['email'], keyId)

        if member:
            newBuyer = Buyer.objects.create(member=member, birthday=getBirthdayDate(memberObj['birthday']),
                                            email=memberObj['email'], fcm=memberObj['fcm'],
                                            phoneNumber=memberObj['tel'],
                                            gender=memberObj['gender'])
            newBuyer.save()
            return newBuyer
        else:
            buyer = Member.objects.create_user(memberObj['email'], memberObj['name'], memberKeyId=keyId)
            buyer.set_password(memberObj['tel'])
            buyer.save()
            newBuyer = Buyer.objects.create(member=buyer, birthday=getBirthdayDate(memberObj['birthday']),
                                            email=memberObj['email'], fcm=memberObj['fcm'],
                                            phoneNumber=memberObj['tel'],
                                            gender=memberObj['gender'])
            newBuyer.save()
            return newBuyer

    @staticmethod
    def getAverageAge(buyers):
        try:
            sum = 0
            for index, buyer in enumerate(buyers):
                sum = sum + buyer.getAge()
            return str(round((sum / len(buyers), 2)))
        except:
            return ("No Buyers")

    @staticmethod
    def getGenderRatio(buyers):
        try:
            male = 0
            female = 0
            for index, buyer in enumerate(buyers):
                if buyer.gender == "male":
                    male = male + 1
                else:
                    female = female + 1
            return (str(round((male / (male + female) * 100), 2)) + "%")
        except:
            return ("No Buyers")

    @staticmethod
    def getTransactionListInBuyerList(buyerlist):
        buyers = Buyer.objects.filter(member__id__in=buyerlist)
        transaction_list = []
        if buyers:
            for index, buyer in enumerate(buyers):
                items = buyer.items.all()
                item_list = []
                if items:
                    for index, item in enumerate(items):
                        item_list.append(item.itemName)
                    transaction_list.append(item_list)
        return transaction_list