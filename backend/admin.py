from django.contrib import admin
from .models import OrderItem, Product

# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Product)
# admin.site.register(ShippingAddress)
