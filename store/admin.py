from django.contrib import admin
from .models import Category_list,Authors,Product,ProductImage
# Register your models here.
admin.site.register(Category_list)
admin.site.register(Authors)
admin.site.register(Product)
admin.site.register(ProductImage)
