# reservations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Reservation, ContactMessage
from .forms import ContactForm
from trips.models import Departure

@login_required
def reservation_list(request):
    """
    Affiche les réservations du client connecté (lecture seule).
    """
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

@login_required
def reserve_departure(request, departure_id):
    """
    Permet au client connecté de réserver un départ (actif). 
    """
    # On s'assure que le départ existe et est actif
    departure = get_object_or_404(Departure, id=departure_id, is_active=True)
    if request.method == 'POST':
        # Créer la réservation
        Reservation.objects.create(user=request.user, departure=departure, status='P')
        return redirect('reservations:list')
    # Page de confirmation de réservation
    return render(request, 'reservations/reserve.html', {'departure': departure})

@login_required
def message_list(request):
    """
    Affiche les messages de contact envoyés par le client connecté (filtrés par email).
    """
    messages = ContactMessage.objects.filter(email=request.user.email).order_by('-submitted_at')
    return render(request, 'reservations/message_list.html', {'messages': messages})

@login_required
@require_POST
def delete_message(request, pk):
    """
    Permet au client connecté de supprimer un de ses messages de contact.
    """
    msg = get_object_or_404(ContactMessage, pk=pk, email=request.user.email)
    msg.delete()
    return redirect('reservations:messages')
