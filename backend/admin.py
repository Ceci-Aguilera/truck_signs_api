from django.contrib import admin
from .models import Order, Product, ProductColor, ProductType

# Register your models here.

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductType)
