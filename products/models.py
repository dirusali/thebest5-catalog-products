from django.db import models
from django.contrib.postgres.search import SearchVectorField
from postgres_copy import CopyManager

class Shop(models.Model):
    name = models.CharField(max_length=150)
    logo = models.FileField(blank=True, upload_to='shop_logos/')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.CharField(max_length=50, blank=True, null=True)
    shop = models.ForeignKey
    url = models.URLField(max_length=2000, null=True)
    price = models.FloatField(default=0, null=True)
    old_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=3,null=True)
    name = models.CharField(max_length=2000,null=True)
    brand = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    upc = models.CharField(max_length=12, null=True)
    ean = models.CharField(max_length=13, null=True)
    image = models.URLField(max_length=2000, null=True)
    shipping_cost = models.CharField(max_length=150, null=True)
    stock = models.IntegerField(blank=True, null=True)
    search_vector = SearchVectorField(null=True)
    valid_from = models.CharField(max_length=255, null=True)
    category_name = models.CharField(max_length=255, null=True)
    terms_of_contract = models.CharField(max_length=2000, null=True)
    size_stock_amount = models.FloatField(default=0,null=True)
    aw_image_url = models.URLField(max_length=2000, null=True)
    objects = CopyManager()

    def __str__(self):
        return "<Product> %s - %s %s | %s" % (self.name, self.currency, self.price, self.shop)


COMPRESSION_FORMATS = (
    ('zip', 'ZIP'), # The only one supported by now
)


class AutomaticProductUpdate(models.Model):
    shop = models.ForeignKey(Shop)
    catalog_url = models.URLField(max_length=2000)
    is_compressed = models.BooleanField(default=False)
    compress_format = models.CharField(choices=COMPRESSION_FORMATS, max_length=20, null=True, blank=True)
    delimiter = models.CharField(max_length=2, default=';')
    last_update = models.DateTimeField(null=True, blank=True)
    local_file = models.CharField(max_length=2000, null=True, blank=True)
    records_num = models.PositiveIntegerField(default=0, null=True, blank=True)
    enabled = models.BooleanField(default=True)


