from django.contrib import admin
from .models import TruckItem, OtherProduct, OrderItem

# Register your models here.

admin.site.register(TruckItem)
admin.site.register(OtherProduct)
admin.site.register(OrderItem)
