from rest_framework import serializers
from .models import OrderItem, TruckItem, ItemsToShowInCart, CartToShow

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckItem
        fields = ['nickname']

class ItemsToShowInCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemsToShowInCart
        fields = '__all__'

class CartToShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartToShow
        fields = '__all__'
