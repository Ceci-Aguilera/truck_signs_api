from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'id',
        'ordered',
        'get_product_variation_id',
        'get_product',
        'get_product_category',
        'ordered_date',
    ]

    def get_product_variation_id(self, obj):
        try:
            return obj.product.id
        except:
            return 'No customized product'
    get_product_variation_id.short_description = 'Customized Product ID'
    get_product_variation_id.admin_order_field = 'product__id'

    def get_product(self, obj):
        try:
            return obj.product.product.id
        except:
            return 'No base product'
    get_product.short_description = 'Base Product ID'
    get_product.admin_order_field = 'product__product__id'

    def get_product_category(self, obj):
        try:
            return obj.product.product.category
        except:
            return 'No category'
    get_product_category.short_description = 'Product Category'
    get_product_category.admin_order_field = 'product__product__categotry'

    search_fields = ['user_email', 'id']





class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'base_price',
        'max_amount_of_lettering_items',
        'height',
        'width',
        'id',
    ]
    search_fields = ['title', 'id']





class LetteringItemCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'id',
    ]
    search_fields = ['title', 'id']






class ProductColorAdmin(admin.ModelAdmin):
    list_display = [
        'color_nickname',
        'color_in_hex',
        'id',
    ]
    search_fields = ['color_nickname',  'color_in_hex', 'id']





class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'is_uploaded',
        'id',
    ]
    search_fields = ['title',  'category', 'id']





class ProductVariationAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'get_amount_of_lettering',
        'product_color',
        'get_amount',
        'id',
    ]

    def get_amount(self, obj):
        try:
            return obj.amount
        except:
            return '0'

    get_amount.short_description = "Amount of Product"
    get_amount.admin_order_field = "amount"


    def get_amount_of_lettering(self, obj):
        try:
            return len(obj.get_all_lettering_items())
        except:
            return '0'
    get_amount_of_lettering.short_description = 'Amount of Lettering'
    get_amount_of_lettering.admin_order_field = 'len(obj.get_all_lettering_items())'

    search_fields = ['product',  'product_color', 'id']




class LetteringItemVariationAdmin(admin.ModelAdmin):
    list_display = [
        'get_lettering_item_category',
        'lettering',
        'get_product_variation',
        'id',
    ]

    def get_lettering_item_category(self, obj):
        try:
            return obj.lettering_item_category
        except:
            return "---"

        get_amount_of_lettering.short_description = 'Category'


    def get_product_variation(self, obj):
        try:
            return obj.product_variation
        except:
            return "---"

        get_product_variation.short_description = 'Product Variation'


        search_fields = ['lettering_item_category', 'lettering', 'id']






class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'get_amount',
        'timestamp',
        'id',
    ]

    def get_amount(self, obj):
        try:
            return str(obj.amount / 100.0) + ' USD'
        except:
            return "---"

        get_amount.short_description = 'Amount'

    search_fields = ['user_email', 'id']





class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'text',
        'id',
    ]

    search_fields = ['user_email', 'id']



admin.site.register(Category, CategoryAdmin)
admin.site.register(LetteringItemCategory, LetteringItemCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(LetteringItemVariation, LetteringItemVariationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
