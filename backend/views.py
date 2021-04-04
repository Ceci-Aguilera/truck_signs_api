from django.shortcuts import render
from .models import TruckItem

# Create your views here.

def HomeView(request):

    if request.method == 'GET':
        list_of_trucks = TruckItem.objects.all()
        list_of_trucks_to_show = (truck for truck in list_of_trucks if truck.is_single_image_for_show == True)
        template_name = 'home.html'
        return render(request, template_name, {'list_of_trucks_to_show':list_of_trucks_to_show})
