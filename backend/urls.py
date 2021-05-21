from django.contrib import admin
from django.conf.urls import url,include
from .views import PricesPageAPI,HowToAPIView, CreateOrderAPI, OrderSummaryAPIView, RetrieveAllProductColorsAPI

app_name = 'trucks_signs_app'
urlpatterns = [
    # url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us-view'),
    url(r'^retrieve-product-colors/$', RetrieveAllProductColorsAPI, name='product-colors-api'),
    url(r'^products-price/$', PricesPageAPI, name='prices-api'),
    url(r'^how-to-apply-products/$', HowToAPIView, name='how-to-view'),
    url(r'^create-order/(?P<pk>[0-9]+)/$', CreateOrderAPI, name='create-order-api'),
    url(r'^order-summary/(?P<pk>[0-9]+)/$', OrderSummaryAPIView, name='order-summary'),
    # url(r'^how-to-apply-products/$', HowToView.as_view(), name='how-to-view'),
]
