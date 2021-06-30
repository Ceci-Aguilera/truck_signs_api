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

    lettering_item_category = LetteringItemCategorySerializer(read_only=True)

    class Meta:
        model = LetteringItemVariation
        fields = ('lettering_item_category', 'lettering')


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


class ProductVariationSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    product_color = ProductColorSerializer(read_only=True)
    all_lettering_items = LetteringItemVariationSerializer(source='lettering_item_variation_set', many=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, obj):
        items = obj.get_all_lettering_items()
        price = obj.product.base_price
        for item in items:
            price += item.lettering_item_category.price
        return price

    class Meta:
        model = ProductVariation
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    email_user = serializers.EmailField(required=True)

    class Meta:
        model = Payment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(required=True)
    product = ProductVariationSerializer(read_only=True)
    comment = serializers.CharField(required=False)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
