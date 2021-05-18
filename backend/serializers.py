from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializerNoTruck(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['user','send_email_proof','address1','address2','city','state','zipcode','country','has_truck_item','has_truck_number','has_fire_Extinguisher','has_side_only_letters','comments']


class OrderItemSerializerTruck(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['user','send_email_proof','address1','address2','city','state','zipcode','country','has_truck_item','company_name','dot_number','mc_number','origin','vim_number','has_truck_number','has_fire_Extinguisher','has_side_only_letters','comments']
