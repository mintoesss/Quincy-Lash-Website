from django.contrib import admin
from .models import Service, Client, Appointment

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Appointment)
# Register your models here.
