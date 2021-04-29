from django.contrib import admin
from django.conf.urls import url,include
from .views import HowToAPIView, MakeOrderTruckAPIView, MakeOrderOtherProductAPIView, OrderSummaryAPIView

app_name = 'trucks_signs_app'
urlpatterns = [
    # url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us-view'),
    url(r'^how-to-apply-products/$', HowToAPIView, name='how-to-view'),
    url(r'^create-order/truck/(?P<pk>[0-9]+)/$', MakeOrderTruckAPIView, name='create-order-truck'),
    url(r'^create-order/other-product/(?P<pk>[0-9]+)/$', MakeOrderOtherProductAPIView, name='create-order-product'),
    url(r'^order-summary/(?P<pk>[0-9]+)/$', OrderSummaryAPIView, name='order-summary'),
    # url(r'^how-to-apply-products/$', HowToView.as_view(), name='how-to-view'),
    # url(r'^prices-products/$', PricesView.as_view(), name='prices-view'),
]
