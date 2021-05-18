from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from .models import OrderItem, Product
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import OrderItemSerializerTruck, OrderItemSerializerNoTruck
import stripe
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    list_of_products = Product.objects.all()
    list_of_trucks_and_product_prices_to_show = dict()
    list_of_trucks_and_product_prices_to_show['Truck'] = dict()
    list_of_trucks_and_product_prices_to_show['Prices'] = dict()

    for productItem in list_of_products:
        print(productItem.type_of_product)
        if (productItem.type_of_product == 'Truck Logo' and
         productItem.is_single_image_for_show == True):

            truck_url = request.build_absolute_uri(productItem.singleImage.url)

            list_of_trucks_and_product_prices_to_show['Truck'][productItem.nickname] = {}

            list_of_trucks_and_product_prices_to_show['Truck'][productItem.nickname]['nickname'] = productItem.nickname
            list_of_trucks_and_product_prices_to_show['Truck'][productItem.nickname]['url'] = truck_url
            list_of_trucks_and_product_prices_to_show['Truck'][productItem.nickname]['pk'] = productItem.pk

            list_of_trucks_and_product_prices_to_show['Prices']['Truck'] = {}
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['price'] = productItem.price
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['url'] = truck_url
            list_of_trucks_and_product_prices_to_show['Prices']['Truck']['pk'] = productItem.pk

    # Prices to Show
        elif(productItem.is_single_image_for_show == True):
            product_url = request.build_absolute_uri(productItem.singleImage.url)
            list_of_trucks_and_product_prices_to_show['Prices'][productItem.nickname] = {}
            list_of_trucks_and_product_prices_to_show['Prices'][productItem.nickname]['price'] = productItem.price
            list_of_trucks_and_product_prices_to_show['Prices'][productItem.nickname]['url'] = product_url
            list_of_trucks_and_product_prices_to_show['Prices'][productItem.nickname]['pk'] = productItem.pk

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
        truck = Product.objects.get(pk = pk)

        if truck.type_of_product != 'Truck Logo':
            return JsonResponse({'Message':'Error no such item'})

        truck_multy_image_url = request.build_absolute_uri(truck.multiImage.url)
        return JsonResponse({'Message':truck_multy_image_url})

    if request.method == 'POST':
        serializer_of_order = OrderItemSerializerTruck(data=request.data['order'])
        if serializer_of_order.is_valid():
            user_order = serializer_of_order.save()


            truck = Product.objects.get(pk = pk)
            user_order.total_cost += truck.price

            if(user_order.has_truck_number == True):
                user_order.truck_number = data['truck_number']
                number_price = OtherProduct.objects.get(nickname = 'Truck Number')
                user_order.total_cost += number_price

            if(user_order.has_fire_Extinguisher == True):
                fire_extinguisher_price = OtherProduct.objects.get(nickname = 'Fire Extinguisher')
                user_order.total_cost += fire_extinguisher_price

            if(user_order.has_side_only_letters == True):
                side_only_letters_price = Product.objects.get(nickname = 'Side Only Letters')
                user_order.total_cost += side_only_letters_price

            user_order.save()
            order_pk = str(user_order.pk)

            # Go to Cart View before checkout
            return JsonResponse({'message': 'Order made', 'order_pk': order_pk})

        return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)



@api_view(['GET','POST'])
def MakeOrderOtherProductAPIView(request,pk):

    if request.method == 'GET':
        product = Product.objects.get(pk = pk)

        if product.type_of_product == 'Truck Logo':
            return JsonResponse({'Message':'Error no such item'})

        product_multy_image_url = request.build_absolute_uri(product.multiImage.url)
        return JsonResponse({'Message':product_multy_image_url})

    if request.method == 'POST':
        serializer_of_order = OrderItemSerializerNoTruck(data=request.data['order'])
        if serializer_of_order.is_valid():
            user_order = serializer_of_order.save()

            if(user_order.has_truck_number == True):
                user_order.truck_number = data['truck_number']
                number_price = Product.objects.get(nickname = 'Truck Number')
                user_order.total_cost += number_price

            if(user_order.has_fire_Extinguisher == True):
                fire_extinguisher_price = Product.objects.get(nickname = 'Fire Extinguisher')
                user_order.total_cost += fire_extinguisher_price

            if(user_order.has_side_only_letters == True):
                side_only_letters_price = Product.objects.get(nickname = 'Side Only Letters')
                user_order.total_cost += side_only_letters_price

            user_order.save()
            order_pk = str(user_order.pk)

            # Go to Cart View before checkout
            return JsonResponse({'message': 'Order made', 'order_pk': order_pk})
        return Response({'message': 'Error processing order'}, status=status.HTTP_201_CREATED)



# Here is the Cart View before buying to review if order is OK
#   The data displayed will be : Items with prices, total amount, user email and
#   shipping address. After pressing checkout buttom the payment process will
#   begin.


@api_view(['GET','POST'])
def OrderSummaryAPIView(request,pk):


    order = OrderItem.objects.get(pk = pk)
    # cart = CartToShow(user_email = order.user, total_cost = order.total_cost)
    info_to_display = dict()
    info_to_display['items'] = dict()

    if order.has_truck_item == True:
        truck = order.truck
        info_to_display['items']['truck'] = str(truck.price)
    else:
        info_to_display['items']['truck'] = '0.0'

    if order.has_truck_number == True:
        item = Product.objects.get(nickname = 'Truck Number')
        info_to_display['items']['truck_number'] = str(item.price)
    else:
        info_to_display['items']['truck_number'] = '0.0'

    if order.has_fire_Extinguisher == True:
        item = Product.objects.get(nickname = 'Fire Extinguisher')
        info_to_display['items']['fire_extinguisher'] = str(item.price)
    else:
        info_to_display['items']['fire_extinguisher'] = '0.0'

    if order.has_side_only_letters == True:
        item = Product.objects.get(nickname = 'Side Only Letters')
        info_to_display['items']['side_only_letters'] = str(item.price)
    else:
        info_to_display['items']['side_only_letters'] = '0.0'

    info_to_display['total_cost'] = order.total_cost
    info_to_display['user'] = order.user
    info_to_display['address1'] = order.address1
    info_to_display['address2'] = order.address2
    info_to_display['address3'] = order.city+', '+order.zipcode+', '+order.state

    if request.method == "GET":
        return Response(info_to_display, status=status.HTTP_201_CREATED)

    elif request.method == "POST":
        card_num = request.data['card_num']
        exp_month = request.data['exp_month']
        exp_year = request.data['exp_year']
        cvc = request.data['cvc']

        token = stripe.Token.create(
          card={
            "number": card_num,
            "exp_month": int(exp_month),
            "exp_year": int(exp_year),
            "cvc": cvc
          },
        )

        amount_to_charge = int(order.total_cost * 100)

        charge = stripe.Charge.create(
          amount=amount_to_charge,
          currency="usd",
          source=token,
          description="Purchase at truck-sings.com"
        )

        if charge['captured'] == True:

            #Send Confirmation Email
            subject = 'Truck Signs Purchase'
            message = f'Hi, thank you for purchasing at Truck Signs.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['seampler.test@protonmail.com', ]
            send_mail( subject, message, email_from, recipient_list )

            return JsonResponse({'message':'Order Done'})

        return JsonResponse({'message':'Error in order'})
