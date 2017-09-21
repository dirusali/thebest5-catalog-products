from rest_framework import serializers
from .models import Product, Shop


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('shop','url','price', 'old_price', 'currency', 'name', 'description', 'upc', 'ean', 'image', 'shipping_cost', 'stock',)

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
