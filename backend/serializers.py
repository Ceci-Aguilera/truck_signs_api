from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    sample_product_id = serializers.SerializerMethodField('get_sample_product_id')

    def get_sample_product_id(self, obj):
        product = Product.objects.filter(category=obj).first()
        return product.id

    class Meta:
        model = Category
        fields = ('title', 'image', 'base_price', 'max_amount_of_lettering_items', 'height', 'width', 'sample_product_id')


class LetteringItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LetteringItemCategory
        fields = '__all__'


class LetteringItemVariationSerializer(serializers.ModelSerializer):

    lettering_item_category = LetteringItemCategorySerializer(read_only=True)

    class Meta:
        model = LetteringItemVariation
        fields = ('lettering_item_category', 'lettering')




class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(use_url=True)
    detail_image = serializers.ImageField(use_url=True)
    product_color_default = ProductColorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'




class ProductVariationSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    product_color = ProductColorSerializer(read_only=True)
    all_lettering_items = LetteringItemVariationSerializer(source='lettering_item_variation_set', many=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, obj):
        items = obj.get_all_lettering_items()
        price = obj.product.category.base_price
        for item in items:
            price += item.lettering_item_category.price
        price = price * obj.amount
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


class CommentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(required=True)
    image = serializers.ImageField(use_url=True)
    text = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
