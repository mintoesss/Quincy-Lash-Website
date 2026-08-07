from django.shortcuts import render, redirect  # redirect was missing
from .models import Service, Client, Appointment


def service_list(request):
    if request.method == "POST":
        print(request.POST)

        # STEP 1 — pull the submitted values out of request.POST
        # request.POST is a dictionary. The keys are the name= attributes
        # from the form inputs in index.html. Every value arrives as a STRING.
        client_name = request.POST["client_name"]
        client_phone = request.POST["client_phone"]
        client_email = request.POST["client_email"]
        service_id = request.POST["service_id"]
        start_time = request.POST["start_time"]

        # STEP 2 — turn the service_id string into a real Service object
        # The form sent '1' (a string). Appointment.service is a ForeignKey,
        # which points at an OBJECT, not a string. So we ask the database
        # for the row with that id and get the actual Service back.
        service = Service.objects.get(id=service_id)

        # STEP 3 — find this client, or create them if they're new
        # Returns a TUPLE: (the object, True/False for whether it was created)
        # email= is the LOOKUP field — what it searches by
        # defaults= is only used IF it has to create a new row
        client, created = Client.objects.get_or_create(
            email=client_email,
            defaults={
                "name": client_name,
                "phone": client_phone,
            }
        )

        # STEP 4 — create the Appointment row
        # This is the actual database WRITE. Everything above was prep.
        # client= and service= take OBJECTS, not ids — that's why steps 2 and 3 exist.
        # price_at_booking copies the price NOW so it's frozen forever.
        Appointment.objects.create(
            client=client,
            service=service,
            start_time=start_time,
            price_at_booking=service.price,
        )

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