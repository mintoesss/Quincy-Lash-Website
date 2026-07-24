from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) # blank=True means this field is allowed to be empty when form is filled out
    duration_minutes = models.PositiveIntegerField() # makes sure it is never negative
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True) # soft delete: she doesn't delete a service, she flips this to False and it disappears from the booking page. Row stays so old appointments still work

    def __str__(self): # dunder method
        return f"{self.name} (${self.price})"


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True) # they don't have to provide a phone number, phone / zip codes have to be CharField, not int because of dashes / ()
    notes = models.TextField(blank=True) # don't have to provide notes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.email}"


class Appointment(models.Model):
    STATUS_CHOICES = [ # constant variable
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments") # on_delete=models.CASCADE -> takes care of when the row gets deleted, related_name rename for easier reverse_lookup client.appointments.all()
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments") # on_delete=models.PROTECT, Django refuses to delete the parent if children exist: if you delete the service, all of her appointments still need to know what they were for
    start_time = models.DateTimeField() # stores a date and time
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    price_at_booking = models.DecimalField(max_digits=6, decimal_places=2) # snapshot of what she was actually charged. If mom raises prices later, old appointments keep the real historical price
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.client.name} — {self.service.name} on {self.start_time:%b %d, %Y at %I:%M %p}"