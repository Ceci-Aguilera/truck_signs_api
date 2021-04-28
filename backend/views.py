from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from .models import TruckItem, OtherProduct
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import OrderItemSerializerTruck, OrderItemSerializerNoTruck, TruckSerializer

# Create your views here.

# HomePageAPI contains the list of Logos and Prices of items.
#   The map list_of_trucks_and_product_prices_to_show['Truck'] has the info of
#   the trucks logos and the map  The map list_of_trucks_and_product_prices_to_show['Prices']
#   has the info of all generic objects prices (this second map was suppose to
#   be in the PricesView)
#
#   From here if image is pressed redirect to either create-order/truck/pk/ or
#   create-order/other-product/pk/

@api_view(['GET'])
def HomePageAPI(request):

    list_of_trucks = TruckItem.objects.all()
    list_of_trucks_and_product_prices_to_show = dict()
    list_of_trucks_and_product_prices_to_show['Truck'] = dict()
    list_of_trucks_and_product_prices_to_show['Prices'] = dict()

    for truck in list_of_trucks:
        if truck.is_single_image_for_show == True:

            truck_url = request.build_absolute_uri(truck.singleImage.url)

            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname] = {}

            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['nickname'] = truck.nickname
            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['url'] = truck_url
            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['pk'] = truck.pk

            list_of_trucks_and_product_prices_to_show['Prices']['Truck'] = {}
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['price'] = truck.price
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['url'] = truck_url
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['pk'] = truck.pk

    # Prices to Show

    list_of_other_products = list_of_trucks = OtherProduct.objects.all()
    for product in list_of_other_products:
        product_url = request.build_absolute_uri(product.singleImage.url)
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname] = {}
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['price'] = product.price
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['url'] = product_url
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['pk'] = product.pk

    template_name = 'home.html'

    return Response(list_of_trucks_and_product_prices_to_show,status=status.HTTP_201_CREATED)


@api_view(['GET'])
def HowToAPIView(request):
    return Response({}, status=status.HTTP_201_CREATED)

# class ContactUsView(TemplateView):
#     template_name = 'contact_us.html'

# class HowToView(TemplateView):
#     template_name = 'how_to.html'

# class PricesView(TemplateView):
#     template_name = 'prices.html'




# MakeOrderAPIView (Truck and Other Product) is for complete two forms: First
#   the Order form in which to select the objects to purchase (Logo or another
#   Item must be already selected)
#
#   In Get method give Logo or Item info and in Post select especifications to
#   make the purchase.
#
#   The info passed in Post will be in 2 json files: data['order'] for the order
#   serializer and data['truck_number'] with the number of the truck in case of
#   having truck number.
#
#   From here redirect to Confirm Order and Checkout after Post method or not in
#   case of error response.

@api_view(['GET','POST'])
def MakeOrderTruckAPIView(request,pk):

    if request.method == 'GET':
        truck = TruckItem.objects.get(pk = pk)
        truck_multy_image_url = request.build_absolute_uri(truck.multiImage.url)
        return JsonResponse({'Image Link':truck_multy_image_url})

    if request.method == 'POST':
        serializer_of_order = OrderItemSerializerTruck(data=request.data['order'])
        if serializer_of_order.is_valid():
            user_order = serializer_of_order.save()


            truck = TruckItem.objects.get(pk = pk)
            user_order.total_cost += truck.price

            if(user_order.has_truck_number == True):
                user_order.truck_number = data['truck_number']
                number_price = OtherProduct.objects.get(nickname = 'Truck Number')
                user_order.total_cost += number_price

            if(user_order.has_fire_Extinguisher == True):
                fire_extinguisher_price = OtherProduct.objects.get(nickname = 'Fire Extinguisher')
                user_order.total_cost += fire_extinguisher_price

            user_order.save()

            # Go to Cart View before checkout
            return JsonResponse({'message': 'Order made'})

        return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)



@api_view(['GET','POST'])
def MakeOrderOtherProductAPIView(request,pk):

    if request.method == 'GET':
        product = OtherProduct.objects.get(pk = pk)
        product_multy_image_url = request.build_absolute_uri(product.multiImage.url)
        return JsonResponse({'Image Link':product_multy_image_url})

    if request.method == 'POST':
        serializer_of_order = OrderItemSerializerNoTruck(data=request.data['order'])
        if serializer_of_order.is_valid():
            user_order = serializer_of_order.save()

            if(user_order.has_truck_number == True):
                user_order.truck_number = data['truck_number']
                number_price = OtherProduct.objects.get(nickname = 'Truck Number')
                user_order.total_cost += number_price

            if(user_order.has_fire_Extinguisher == True):
                fire_extinguisher_price = OtherProduct.objects.get(nickname = 'Fire Extinguisher')
                user_order.total_cost += fire_extinguisher_price

            user_order.save()

            # Go to Cart View before checkout
            return JsonResponse({'message': 'Order made'})
        return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)
