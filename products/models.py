from django.db import models
import csv
import io
from django.conf import settings
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel


def upload_csv_file(instance, filename):
    qs = instance.__class__.objects.filter(user=instance.user)
    if qs.exists():
        num_ = qs.last().id + 1
    else:
        num_ = 1
    #return f'csv/{num_}/{instance.shop.name}/{filename}'
    return "csv"

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



def convert_header(csvHeader):
    header_ = csvHeader
    cols = []
    for i, h in enumerate(header_):
        col = h.replace(' ', '_').lower()
        header_[i] = col
        if col == 'picture':
            header_[i] = 'image'
        if col == 'currencyid':
            header_[i] = 'currency'
        if col == 'oldprice':
            header_[i] = 'old_price'
    return header_


def csv_upload_post_save(sender, instance, created, *args, **kwargs):
    if not instance.completed:
        csv_file = instance.file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=';')
        header_ = next(reader)
        header_cols = convert_header(header_)
        for row in reader:
            try:
                obj = Product()
                obj.shop = instance.shop
                for i, field in enumerate(row):
                    setattr(obj, header_cols[i], field)
                obj.save()
            except:
                print('error')
            
        instance.completed = True
        instance.save()


post_save.connect(csv_upload_post_save, sender=CSVUpload)
