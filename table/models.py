from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Test(TimeStampedModel):
    testfield = models.CharField(max_length=200, default="")

    @staticmethod
    def createTest(testfield):
        obj = Test.objects.create(testfield=testfield)
        obj.save()