from django.contrib import admin
from .models import Shop, Product

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ean', 'shop')
    list_filter = ('shop',)
    search_fields = ('name',)
    
admin.site.register(Product, ProductAdmin)
