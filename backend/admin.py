from django.contrib import admin
from .models import TruckItem, OtherProduct, OrderItem, ItemsToShowInCart, CartToShow

# Register your models here.

admin.site.register(TruckItem)
admin.site.register(OtherProduct)
admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
