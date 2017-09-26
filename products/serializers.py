from rest_framework import serializers
from .models import Product, Shop

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    shop = ShopSerializer(required = False)
    
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('shop','url','price', 'old_price', 'currency', 'name', 'description', 'upc', 'ean', 'image', 'shipping_cost', 'stock',)

