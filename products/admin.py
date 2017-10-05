from django.contrib import admin
from .models import Shop, Product, AutomaticProductUpdate


# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ean', 'shop')
    list_filter = ('shop',)
    search_fields = ('name',)
    
admin.site.register(Product, ProductAdmin)


class AutomaticProductUpdateAdmin(admin.ModelAdmin):
    list_display = ('shop', 'catalog_url', 'delimiter', 'is_compressed', 'compress_format', 'last_update', 'local_file', 'enabled')
    list_filter = ('shop',)
admin.site.register(AutomaticProductUpdate, AutomaticProductUpdateAdmin)
