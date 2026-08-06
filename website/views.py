from django.shortcuts import render, redirect  # redirect was missing
from .models import Service, Client, Appointment


def service_list(request):
    if request.method == "POST":
        print(request.POST)
        # read the submitted data
        # create the Client
        # create the Appointment
        return redirect("service_list")

    # Breaking down Service.objects.filter(is_active=True)
    # Service = model class / table
    # objects = the model's manager, every model gets one, entire job is fetching, filtering, and counting rows
    # .filter(is_active=True) = return the rows where is_active column is True
    # store it in a variable called services, to be used in an html page
    services = Service.objects.filter(is_active=True)

    return render(request, "website/index.html", {
        "services": services,
    })