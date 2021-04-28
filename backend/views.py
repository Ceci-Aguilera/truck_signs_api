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
#   The map list_of_trucks_and_product_prices_to_show['Truck'] has the info of
#   the trucks logos and the map  The map list_of_trucks_and_product_prices_to_show['Prices']
#   has the info of all generic objects prices (this second map was suppose to
#   be in the PricesView)

@api_view(['GET'])
def HomePageAPI(request):

    list_of_trucks = TruckItem.objects.all()
    list_of_trucks_and_product_prices_to_show = dict()
    list_of_trucks_and_product_prices_to_show['Truck'] = dict()
    list_of_trucks_and_product_prices_to_show['Prices'] = dict()

    for truck in list_of_trucks:
        if truck.is_single_image_for_show == True:

            truck_url = request.build_absolute_uri(truck.singleImage.url)
            truck_multy_url = request.build_absolute_uri(truck.multiImage.url)

            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname] = {}

            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['nickname'] = truck.nickname
            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['url'] = truck_url
            list_of_trucks_and_product_prices_to_show['Truck'][truck.nickname]['multy_url'] = truck_multy_url

            list_of_trucks_and_product_prices_to_show['Prices']['Truck'] = {}
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['price'] = truck.price
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['url'] = truck_url

    # Prices to Show

    list_of_other_products = list_of_trucks = OtherProduct.objects.all()
    for product in list_of_other_products:
        product_url = request.build_absolute_uri(product.singleImage.url)
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname] = {}
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['price'] = product.price
        list_of_trucks_and_product_prices_to_show['Prices'][product.nickname]['url'] = product_url

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




# MakeOrderAPIView is for complete two forms: First the Order form in which to
# select the objects to purchase (Logo or another Item must be already selected)
#   In Get method give Logo or Item info and in Post select especifications to
#   make the purchase (First Form).
#   The second Form has the info of the Shipping Address
#   From here redirect to Confirm Order and Checkout after Post method

@api_view(['POST'])
def MakeOrderAPIView(request):
    serializer_of_order = OrderItemSerializer(data=request.data['order'])
    if serializer_of_order.is_valid():
        serializer_of_order.save()
        # Go to Cart View before checkout
        user_email = request.data['user_email']

        return JsonResponse({'message': 'Order made'})
    return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)
