from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import TruckItem, OtherProduct
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.

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

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

class HowToView(TemplateView):
    template_name = 'how_to.html'

class PricesView(TemplateView):
    template_name = 'prices.html'
