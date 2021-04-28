from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import TruckItem, OtherProduct
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import OrderItemSerializer, TruckSerializer

# Create your views here.

# HomePageAPI contains the list of Logos and Prices of items.
@api_view(['GET'])
def HomePageAPI(request):
    list_of_trucks = TruckItem.objects.all()
    list_of_trucks_and_product_prices_to_show = dict()
    list_of_trucks_and_product_prices_to_show['Truck'] = dict()
    list_of_trucks_and_product_prices_to_show['Prices'] = dict()
    for truck in list_of_trucks:
        if truck.is_single_image_for_show == True:
            truck_url = request.build_absolute_uri(truck.singleImage.url)
            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname] = truck_url
            list_of_trucks_and_product_prices_to_show['Prices']['Truck'] = {}
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['price'] = truck.price
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['url'] = truck_url


    list_of_other_products = list_of_trucks = OtherProduct.objects.all()
    for product in list_of_other_products:
        product_url = request.build_absolute_uri(product.singleImage.url)
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname] = {}
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['price'] = product.price
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['url'] = product_url

    template_name = 'home.html'

    return Response(list_of_trucks_and_product_prices_to_show,status=status.HTTP_201_CREATED)



# class ContactUsView(TemplateView):
#     template_name = 'contact_us.html'

@api_view(['GET'])
def HowToAPIView(request):
    return Response({}, status=status.HTTP_201_CREATED)

# class HowToView(TemplateView):
#     template_name = 'how_to.html'

# class PricesView(TemplateView):
#     template_name = 'prices.html'

@api_view(['GET','POST'])
def MakeOrderAPIView(request):
    if request.method == 'GET':
        try:
            selected_item = TruckItem.objects.get(nickname=request.data['nickname'])
        except TruckItem.DoesNotExist:
            try:
                selected_item = OtherProduct.objects.get(nickname=request.data['nickname'])
            except Truck.DoesNotExist:
                selected_item = 'NONE'
        if selected_item != 'NONE':
            return Response({'item_selected': 'NONE'}, status=status.HTTP_201_CREATED)

        return Response({'item_selected': selected_item.nickname}, status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data['order'])
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order made'})
        return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)
