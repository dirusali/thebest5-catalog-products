from django.db import models
import csv
import io
from django.conf import settings
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel


def upload_csv_file(instance, filename):
    return "csv/{0}/{1}".format(instance.shop.id,filename)

class Shop(models.Model):
    name = models.CharField(max_length=150)
    logo = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    shop = models.ForeignKey(Shop)
    url = models.URLField()
    price = models.FloatField(default=0)
    old_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=3,blank=True)
    name = models.CharField(max_length=255,blank=True)
    description = models.CharField(max_length=500,blank=True)
    upc = models.CharField(max_length=150, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    image = models.URLField(blank=True)
    shipping_cost = models.CharField(max_length=150, blank=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class CSVUpload(TimeStampedModel):
    file = models.FileField(upload_to=upload_csv_file)
    shop = models.ForeignKey(Shop)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.shop, self.created)





