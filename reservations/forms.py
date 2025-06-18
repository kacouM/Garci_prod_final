
from django import forms
from .models import ContactMessage, Reservation

class ContactForm(forms.ModelForm):
    """Formulaire de contact (section Contact)."""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

# (Optionnel) Formulaire de réservation
class ReservationForm(forms.ModelForm):
    """Formulaire pour réserver un départ (peut être intégré dans la vue)."""
    class Meta:
        model = Reservation
        fields = []
