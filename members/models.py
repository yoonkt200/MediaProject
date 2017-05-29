from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth import authenticate, login
import datetime

from commerce.models import CategoryDivision, Category, Item

GENDER = (
    ('M', '남자'),
    ('W', '여자'),
)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MemberDivision(TimeStampedModel):
    divisionName = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.divisionName


class MemberManager(BaseUserManager):
    def create_user(self, userId, memberName, password=None):
        if not userId:
            raise ValueError('Users must have an ID')

        user = self.model(userId=userId, memberName=memberName)

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
    memberKeyId = models.CharField(max_length=200, default="", unique=True)

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


class Seller(TimeStampedModel):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, )
    birthday = models.DateField(default=datetime.date.today)
    email = models.EmailField(verbose_name='email address', max_length=200)
    fcm = models.CharField(blank=True, max_length=200)
    gender = models.CharField(max_length=200, choices=GENDER, default="남자")
    isLocationAgree = models.BooleanField(default=False)
    isPushAgree = models.BooleanField(default=False)
    phoneNumber = models.CharField(blank=True, max_length=200)

    address = models.CharField(blank=True, default="", max_length=200)
    category = models.ForeignKey(Category, default=1)

    def __str__(self):
        return self.member.memberName + "/" + self.phoneNumber


class Buyer(TimeStampedModel):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, )
    birthday = models.DateField(default=datetime.date.today)
    email = models.EmailField(verbose_name='email address', max_length=200)
    fcm = models.CharField(blank=True, max_length=200)
    gender = models.CharField(max_length=200, choices=GENDER, default="남자")
    isLocationAgree = models.BooleanField(default=False)
    isPushAgree = models.BooleanField(default=False)
    phoneNumber = models.CharField(blank=True, max_length=200)

    items = models.ManyToManyField('commerce.Item')

    class Meta:
        ordering = ['member']

    def __str__(self):
        return self.member.memberName