from django.db import models
from django.conf import settings
from trips.models import Departure

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Message de {self.name} ({self.email})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('P', 'En attente'),
        ('C', 'Confirmée'),
        ('X', 'Annulée'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réservation #{self.id} - {self.departure}"
