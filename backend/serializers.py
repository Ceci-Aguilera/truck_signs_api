from rest_framework import serializers
from .models import OrderItem, TruckItem

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckItem
        fields = ['nickname']
