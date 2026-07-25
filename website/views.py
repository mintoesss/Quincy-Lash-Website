from django.shortcuts import render
from .models import Service, Client, Appointment

# Breaking down Service.objects.filter(is_active=True)
# Service = model class / table
# objects = the model's manager, every model gets one, entire job is fetching, filtering, and counting rows
# .filter(is_active=True) = return the rows where is_active column is True
# store it in a variable called services, to be used in an html page
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, "website/index.html", {
        "services": services,
    })