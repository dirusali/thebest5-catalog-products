from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=150)
    logo = models.FileField(blank=True, upload_to='shop_logos/')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.CharField(max_length=50, blank=True, null=True)
    shop = models.ForeignKey(Shop)
    url = models.URLField(max_length=2000)
    price = models.FloatField(default=0)
    old_price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=3,blank=True)
    name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=12, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    image = models.URLField(max_length=2000, blank=True)
    shipping_cost = models.CharField(max_length=150, blank=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "<Product> %s - %s %s | %s" % (self.name, self.currency, self.price, self.shop)
    






