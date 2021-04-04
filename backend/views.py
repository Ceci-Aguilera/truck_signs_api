from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import TruckItem

# Create your views here.

def HomeView(request):

    if request.method == 'GET':
        list_of_trucks = TruckItem.objects.all()
        list_of_trucks_to_show = (truck for truck in list_of_trucks if truck.is_single_image_for_show == True)
        template_name = 'home.html'
        return render(request, template_name, {'list_of_trucks_to_show':list_of_trucks_to_show})

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

class HowToView(TemplateView):
    template_name = 'how_to.html'

class PricesView(TemplateView):
    template_name = 'prices.html'
