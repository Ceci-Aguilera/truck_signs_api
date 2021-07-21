from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

class CategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()

class LetteringItemCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = LetteringItemCategorySerializer
    model = LetteringItemCategory
    queryset = LetteringItemCategory.objects.all()

class ProductListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.all()

class ProductFromCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        return Product.objects.filter(category__id=category_id)


class ProductColorListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductColorSerializer
    model = ProductColor
    queryset = ProductColor.objects.all()


class LogoListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    queryset = Product.objects.filter(category__title='Truck Sign')


class ProductDetail(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'id'
    queryset = Product.objects.all()



# Creates the Product Variation and the Lettering Item Variation, then
# creates the Order
class CreateProductVariationView(GenericAPIView):

    authentication_classes = []
    serializer_class = ProductVariationSerializer

    def post(self, request, format=None):
        data = request.data

        try:
            product_id = data['product_id']
            product = Product.objects.get(id=product_id)
            product_variation = ProductVariation(product=product)
            product_variation.save()

            try:
                lettering_items = data['lettering_items']
                for item in lettering_items:
                    item_serializer = LetteringItemVariationSerializer(data=item)
                    item_serializer.is_valid(raise_exception=True)
                    item_category = LetteringItemCategory.objects.get(id=item_category_id)
                    lettering_item = item_serializer.save(product_variation = product_variation, lettering_item_category=item_category)

            except:
                pass

            try:
                product_color_id = data['product_color_id']
                product_color = ProductColor.objects.get(id=product_color_id)
                product_variation.product_color = product_color

            except:
                pass
            product_variation.save()
            product_variation_serializer = self.get_serializer(product_variation)

            order_serializer = OrderSerializer(data=data['order'])
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save(product=product_variation)

            return Response({"Result": order.id}, status=status.HTTP_200_OK)

        except:
            return Response({"Result": "Error"}, status=status.HTTP_400_BAD_REQUEST)



class PaymentView(GenericAPIView):

    authentication_classes = []
    serializer_class = PaymentSerializer

    def get(self, post, id, format=None):
        order = Order.objects.get(id=id)
        order_serializer = OrderSerializer(order)
        return Response({"Order": order_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):

        try:
            order = Order.objects.get(id=id)

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

            amount = int(order.get_total_price() * 100)

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )

            stripe_charge_id = charge['id']
            payment = Payment(user_email = order.user_email, stripe_charge_id=stripe_charge_id, amount=amount)
            payment.save()
            order.ordered = True
            order.payment = payment
            order.save()
            return Response({"Result": "Success"}, status=status.HTTP_200_OK)

            # Send Email to user

        except stripe.error.CardError as e:
            return Response({"Result":"Error with card during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            return Response({"Result":"Rate Limit error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            return Response({"Result":"Invalid request error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            return Response({"Result":"Authentication error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            return Response({"Result":"API connection error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({"Result":"Something went wrong during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"Result":"Error during payment"}, status=status.HTTP_400_BAD_REQUEST)




class CommentsView(ListAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    model = Comment
    queryset = Comment.objects.all().filter(visible=True)


class CommentCreateView(CreateAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
