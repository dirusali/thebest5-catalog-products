from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Shop(models.Model):
    name = models.CharField(max_length=150)
    logo = models.FileField(blank=True, upload_to='shop_logos/')
    language = models.CharField(max_length=150, default='spanish', blank=True, help_text='language to use in full text search')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.CharField(max_length=50, blank=True, null=True)
    shop = models.ForeignKey(Shop)
    url = models.URLField(max_length=2000)
    price = models.FloatField(default=0)
    old_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=3,blank=True)
    name = models.CharField(max_length=2000,blank=True, db_index=True)
    brand = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=12, blank=True, db_index=True)
    ean = models.CharField(max_length=13, blank=True, db_index=True)
    image = models.URLField(max_length=2000, blank=True)
    shipping_cost = models.CharField(max_length=150, blank=True)
    stock = models.IntegerField(blank=True, null=True)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return "<Product> %s - %s %s | %s" % (self.name, self.currency, self.price, self.shop)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_idx'),
        ]

COMPRESSION_FORMATS = (
    ('zip', 'ZIP'), # The only one supported by now
)


class AutomaticProductUpdate(models.Model):
    shop = models.ForeignKey(Shop)
    catalog_url = models.URLField(max_length=2000, unique=True)
    is_compressed = models.BooleanField(default=True)
    compress_format = models.CharField(choices=COMPRESSION_FORMATS, max_length=20, null=True, blank=True, default='zip')
    delimiter = models.CharField(max_length=3, default=',')
    last_update = models.DateTimeField(null=True, blank=True)
    local_file = models.CharField(max_length=2000, null=True, blank=True)
    records_num = models.PositiveIntegerField(default=0, null=True, blank=True)
    enabled = models.BooleanField(default=True)

