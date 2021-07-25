from django.contrib import admin
from django.conf.urls import url,include
# from .views import PricesPageAPI,HowToAPIView, CreateOrderAPI, OrderSummaryAPIView, RetrieveAllProductColorsAPI
from .views import *

app_name = 'trucks_signs_app'

urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view(), name='categories-api'),
    url(r'^lettering-item-categories/$', LetteringItemCategoryListView.as_view(), name='lettering-item-categories-api'),
    url(r'^products/$', ProductListView.as_view(), name='products-api'),
    url(r'^product-lettering/create/$', ProductLetteringCreate.as_view(), name='product-lettering-create-api'),
    url(r'^product-lettering/(?P<id>[0-9]+)/delete/$', LetteringVariationDestroyAPIView.as_view(), name='lettering-variation-delete-api'),
    url(r'^product-category/(?P<id>[0-9]+)/$', ProductFromCategoryListView.as_view(), name='product-category-api'),
    url(r'^product-variation-retrieve/(?P<id>[0-9]+)/$', ProductVariationRetrieveView.as_view(), name='product-category-api'),
    url(r'^product-color/$', ProductColorListView.as_view(), name='product-color-api'),
    url(r'^product-detail/(?P<id>[0-9]+)/$', ProductDetail.as_view(), name='product-detail-api'),
    url(r'^truck-logo-list/$', LogoListView.as_view(), name='truck-logo-list-api'),
    url(r'^product-variation/create/$', CreateProductVariationView.as_view(), name='product-variation-create-api'),
    url(r'^order/(?P<id>[0-9]+)/create/$', CreateOrder.as_view(), name='create-order-api'),
    url(r'^order/(?P<id>[0-9]+)/retrieve/$', RetrieveOrder.as_view(), name='retrieve-order-api'),
    url(r'^order-payment/(?P<id>[0-9]+)/$', PaymentView.as_view(), name='order-payment-api'),
    url(r'^comments/$', CommentsView.as_view(), name='comments-api'),
    url(r'^comment/create/$', CommentCreateView.as_view(), name='comment-create-api'),
    url(r'^upload-customer-image/$', UploadCustomerImage.as_view(), name='upload-customer-image-api'),
]
