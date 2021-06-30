from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Category
        fields = '__all__'


class LetteringItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LetteringItemCategory
        fields = '__all__'


class LetteringItemVariationSerializer(serializers.ModelSerializer):

    lettering_item_category = LetteringItemCategory(read_only=True)

    class Meta:
        model = LetteringItemVariation
        fields = ('lettering_item_category', 'letteting')


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = '__all__'


class ProductVariationSerializer(self.ModelSerializer):

    product = ProductSerializer(read_only=True)
    product_color = ProductColor(read_only=True)
    all_lettering_items = serializers.SerializerMethodField('get_all_lettering_items')
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_all_lettering_items(self, obj):
        return LetteringItemVariationSerializer(obj.letteringitemvariation__set.all(), many=True, read_only=True)

    def get_total_price(self, obj):
        items = obj.get_all_lettering_items()
        price = obj.product__base_price()
        for item in items:
            price += item.lettering_item_category__price
        return price

    class Meta:
        model = ProductVariation
        fields = '__all__'


class PaymentSerializer(self.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class OrderSerializer(self.ModelSerializer):

    product = ProductVariationSerializer(read_only=True)
    comment = serializers.CharField()
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'






# class OrderPkSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(min_value=0, max_value=None)
#
# class TruckSingleImageSerializer(serializers.Serializer):
#     single_image = serializers.ImageField(use_url=True)
#     pk = serializers.IntegerField(min_value=0, max_value=None)
#
# class ProductSingleImageSerializer(serializers.Serializer):
#     name_of_type_of_product = serializers.CharField(max_length=256)
#     single_image = serializers.ImageField(use_url=True)
#     pk = serializers.IntegerField(min_value=0, max_value=None)
#
# class ProductSerializer(serializers.ModelSerializer):
#
#     name_of_type_of_product = serializers.CharField(source='type_of_product.name_of_type_of_product')
#     base_price = serializers.FloatField(source='type_of_product.base_price')
#     is_company_name_enable = serializers.BooleanField(source='type_of_product.is_company_name_enable')
#     company_name_price = serializers.FloatField(source='type_of_product.company_name_price')
#     is_dot_number_enable = serializers.BooleanField(source='type_of_product.is_dot_number_enable')
#     dot_number_price = serializers.FloatField(source='type_of_product.dot_number_price')
#     is_mc_number_enable = serializers.BooleanField(source='type_of_product.is_mc_number_enable')
#     mc_number_price = serializers.FloatField(source='type_of_product.mc_number_price')
#     is_origin_enable = serializers.BooleanField(source='type_of_product.is_origin_enable')
#     origin_price = serializers.FloatField(source='type_of_product.origin_price')
#     is_vim_number_enable = serializers.BooleanField(source='type_of_product.is_vim_number_enable')
#     vim_number_price = serializers.FloatField(source='type_of_product.vim_number_price')
#     is_truck_number_enable = serializers.BooleanField(source='type_of_product.is_truck_number_enable')
#     truck_number_price = serializers.FloatField(source='type_of_product.truck_number_price')
#     is_color_enable = serializers.BooleanField(source='type_of_product.is_color_enable')
#     color_price = serializers.FloatField(source='type_of_product.color_price')
#
#
#     class Meta:
#         model = Product
#         fields = ('order_image', 'name_of_type_of_product', 'base_price', 'is_company_name_enable','company_name_price', 'is_dot_number_enable', 'dot_number_price', 'is_mc_number_enable', 'mc_number_price', 'is_origin_enable','origin_price','is_vim_number_enable','vim_number_price','is_truck_number_enable','truck_number_price','is_color_enable','color_price')
#
#
# class OrderSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
# class ProductColorSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ProductColor
#         fields = '__all__'
#
#
# class SummaryOrder(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = ('order_date_made', 'user_email', 'address1', 'address2','city', 'state', 'zipcode' ,'country', 'product_type', 'total_cost')
