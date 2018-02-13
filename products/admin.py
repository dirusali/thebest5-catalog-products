from django.contrib import admin
from .models import Shop, Product, AutomaticProductUpdate


# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    search_fields = ('name',)

admin.site.register(Shop, ShopAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ean', 'shop')
    list_filter = ('shop',)
    search_fields = ('name','ean',)
    
admin.site.register(Product, ProductAdmin)


class AutomaticProductUpdateAdmin(admin.ModelAdmin):
    list_display = ('shop', 'last_update', 'records_num', 'local_file', 'enabled', 'catalog_url',)
    list_filter = ('shop',)
admin.site.register(AutomaticProductUpdate, AutomaticProductUpdateAdmin)
