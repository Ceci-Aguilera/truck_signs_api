from rest_framework import serializers
from .models import OrderItem, TruckItem, ItemsToShowInCart, CartToShow

class OrderItemSerializerNoTruck(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['user','send_email_proof','address1','address2','city','state','zipcode','country','has_truck_item','has_truck_number','has_fire_Extinguisher','comments']


class OrderItemSerializerTruck(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['user','send_email_proof','address1','address2','city','state','zipcode','country','has_truck_item','company_name','dot_number','mc_number','origin','vim_number','has_truck_number','has_fire_Extinguisher','comments']



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
