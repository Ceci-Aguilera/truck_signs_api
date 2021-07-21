from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(LetteringItemCategory)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductVariation)
admin.site.register(LetteringItemVariation)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Comment)
