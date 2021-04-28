from django.contrib import admin
from django.conf.urls import url,include
from .views import HowToAPIView, MakeOrderAPIView

app_name = 'trucks_signs_app'
urlpatterns = [
    # url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us-view'),
    url(r'^how-to-apply-products/$', HowToAPIView, name='how-to-view'),
    url(r'^create-order/$', MakeOrderAPIView, name='create-order')
    # url(r'^how-to-apply-products/$', HowToView.as_view(), name='how-to-view'),
    # url(r'^prices-products/$', PricesView.as_view(), name='prices-view'),
]
