from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from .models import Order, Product, ProductColor, ProductType
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import SummaryOrder, OrderPkSerializer, TruckSingleImageSerializer, ProductSingleImageSerializer,ProductSerializer, OrderSerializer, ProductColorSerializer
import stripe
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

@api_view(['GET'])
def HomePageAPI(request):
    trucks = Product.objects.filter(type_of_product__name_of_type_of_product='Truck Logo').only('single_image','pk')
    serializer = TruckSingleImageSerializer(trucks, many=True, context={'request': request})
    trucksJson = serializer.data
    return Response(trucksJson, status=status.HTTP_201_CREATED)





@api_view(['GET'])
def PricesPageAPI(request):
    products = ProductType.objects.all().only('name_of_type_of_product','single_image','pk')
    serializer = ProductSingleImageSerializer(products, many=True, context={'request': request})
    productsJson = serializer.data
    return Response(productsJson, status=status.HTTP_201_CREATED)






@api_view(['GET'])
def HowToAPIView(request):
    return Response({}, status=status.HTTP_201_CREATED)






@api_view(['GET'])
def RetrieveAllProductColorsAPI(request):
    colors = ProductColor.objects.all()
    colorsJson = ProductColorSerializer(colors, many=True).data
    return Response(colorsJson, status=status.HTTP_201_CREATED)





@api_view(['GET', 'POST'])
def CreateOrderAPI(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        productData = serializer.data
        return Response(productData, status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
        serializer_of_order = OrderSerializer(data=request.data['order'])
        if serializer_of_order.is_valid():
            order = serializer_of_order.save()
            if(data['color'] != 'None'):
                order.product_color = ProductColor.objects.get(pk=request.data['color'])
            order.product = Product.objects.get(pk=pk)
            order.type_of_product = product.type_of_product.name_of_type_of_product
            order.save()
            order_pk = OrderPkSerializer(order.pk).data
            return Response(order_pk, status=status.HTTP_201_CREATED)
        return Response({'message':'Error in order'}, status=status.HTTP_201_CREATED)







@api_view(['GET','POST'])
def OrderSummaryAPIView(request,pk):

    order = Order.objects.get(pk=pk)
    summary_order = SummaryOrder(order)
    summaryOrderJson = summary_order.data

    if request.method == 'GET':
        return Response(summaryOrderJson, status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
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

        if charge['captured'] == True and order.send_email_proof == True:

            #Send Confirmation Email
            subject = 'Truck Signs Purchase'
            message = f'Hi, thank you for purchasing at Truck Signs.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [order.user_email, ]
            send_mail( subject, message, email_from, recipient_list )

            return JsonResponse({'message':'Order Done'})

        return JsonResponse({'message':'Error in order'})
