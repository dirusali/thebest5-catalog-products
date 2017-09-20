from django.contrib import admin
from .models import Shop, Product, CSVUpload

# Register your models here.

class CSVUploadAdmin(admin.ModelAdmin):
    pass

admin.site.register(CSVUpload, CSVUploadAdmin)
    
class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'ean', 'shop')
    list_filter = ('shop',)
    
admin.site.register(Product, ProductAdmin)
