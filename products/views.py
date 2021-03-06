from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from .models import Product, Shop
from .serializers import ProductSerializer, ShopSerializer


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr=['icontains','exact', 'iexact'])

    class Meta:
        model = Product
        fields = ['name', 'ean', 'upc']
        
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Products to be viewed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_class = ProductFilter
    search_fields = ('name',)

class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Shop to be viewed.
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


    
