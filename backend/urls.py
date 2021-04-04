from django.contrib import admin
from django.conf.urls import url,include
from .views import ContactUsView, HowToView, PricesView

app_name = 'trucks_sings_app'
urlpatterns = [
    url(r'^contact-us/$', ContactUsView.as_view(), name='contact-us-view'),
    url(r'^how-to-apply-products/$', HowToView.as_view(), name='how-to-view'),
    url(r'^prices-products/$', PricesView.as_view(), name='prices-view'),
]
