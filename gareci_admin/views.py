from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta, datetime

from trips.models import Bus, Category, Trip, Departure
from reservations.models import ContactMessage, Reservation
from gareci_admin.utils import StaffRequiredMixin
from .forms import ContactReplyForm
from django.contrib.auth import get_user_model


# Gestion des Bus
class BusListView(StaffRequiredMixin, ListView):
    model = Bus
    template_name = 'dashboard/bus_list.html'

class BusCreateView(StaffRequiredMixin, CreateView):
    model = Bus
    fields = ['name', 'capacity']
    template_name = 'dashboard/bus_form.html'
    success_url = reverse_lazy('dashboard:bus_list')

class BusUpdateView(StaffRequiredMixin, UpdateView):
    model = Bus
    fields = ['name', 'capacity']
    template_name = 'dashboard/bus_form.html'
    success_url = reverse_lazy('dashboard:bus_list')

class BusDeleteView(StaffRequiredMixin, DeleteView):
    model = Bus
    template_name = 'dashboard/bus_confirm_delete.html'
    success_url = reverse_lazy('dashboard:bus_list')

# Gestion des Catégories
class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'

class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard:category_list')

# Gestion des Trajets (Trip)
class TripListView(StaffRequiredMixin, ListView):
    model = Trip
    template_name = 'dashboard/trip_list.html'

class TripCreateView(StaffRequiredMixin, CreateView):
    model = Trip
    fields = ['origin', 'destination', 'category', 'description', 'price']
    template_name = 'dashboard/trip_form.html'
    success_url = reverse_lazy('dashboard:trip_list')

class TripUpdateView(StaffRequiredMixin, UpdateView):
    model = Trip
    fields = ['origin', 'destination', 'category', 'description', 'price']
    template_name = 'dashboard/trip_form.html'
    success_url = reverse_lazy('dashboard:trip_list')

class TripDeleteView(StaffRequiredMixin, DeleteView):
    model = Trip
    template_name = 'dashboard/trip_confirm_delete.html'
    success_url = reverse_lazy('dashboard:trip_list')

# Gestion des Départs (Departure)
class DepartureListView(StaffRequiredMixin, ListView):
    model = Departure
    template_name = 'dashboard/departure_list.html'

    def get_queryset(self):
        return Departure.objects.filter(date__gte=now()).order_by('date', 'time')

class DepartureCreateView(StaffRequiredMixin, CreateView):
    model = Departure
    fields = ['trip', 'bus', 'date', 'time', 'is_active']
    template_name = 'dashboard/departure_form.html'
    success_url = reverse_lazy('dashboard:departure_list')

class DepartureUpdateView(StaffRequiredMixin, UpdateView):
    model = Departure
    fields = ['trip', 'bus', 'date', 'time', 'is_active']
    template_name = 'dashboard/departure_form.html'
    success_url = reverse_lazy('dashboard:departure_list')

class DepartureDeleteView(StaffRequiredMixin, DeleteView):
    model = Departure
    template_name = 'dashboard/departure_confirm_delete.html'
    success_url = reverse_lazy('dashboard:departure_list')

# Consultation des Messages clients
class MessageListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/message_list.html'
    context_object_name = 'messages'
    ordering = ['-submitted_at']

class MessageReplyView(StaffRequiredMixin, UpdateView):
    model = ContactMessage
    form_class = ContactReplyForm
    template_name = 'dashboard/message_form.html'
    success_url = reverse_lazy('dashboard:message_list')

    def form_valid(self, form):
        response = form.save(commit=False)
        response.replied_at = timezone.now()
        # Vérification de la réponse
        if not response.reply:
            return self.form_invalid(form)
        
        response.save()
        
        # Envoi de l'email au client
        try:
            send_mail(
                subject='Réponse à votre message de contact - Gareci',
                message=f"""Bonjour {response.name},

Voici notre réponse à votre message du {response.submitted_at}:

{response.reply}

Cordialement,
L'équipe Gareci""",
                from_email=None,  # Utilise DEFAULT_FROM_EMAIL
                recipient_list=[response.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")  # Pour debug
            
        return super().form_valid(form)

class MessageDeleteView(StaffRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = 'dashboard/message_confirm_delete.html'
    success_url = reverse_lazy('dashboard:message_list')

# Consultation des Réservations clients
class ReservationAdminListView(StaffRequiredMixin, ListView):
    model = Reservation
    template_name = 'dashboard/reservation_list.html'
    context_object_name = 'reservations'
    ordering = ['-booked_at']

class ReservationAdminUpdateView(StaffRequiredMixin, UpdateView):
    model = Reservation
    fields = ['status']
    template_name = 'dashboard/reservation_form.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:index')

class ReservationAdminDeleteView(StaffRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'dashboard/reservation_confirm_delete.html'
    success_url = reverse_lazy('dashboard:reservation_list')

class ReservationAdminConfirmView(StaffRequiredMixin, TemplateView):
    def post(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.status = 'C'
        reservation.save()
        return redirect('dashboard:index')

# Vue du Tableau de Bord
class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        CustomUser = get_user_model()
        context['empty'] = []  # Liste vide pour le filtre default_if_none
          # Statistiques rapides
        context['total_reservations'] = Reservation.objects.count()
        context['total_users'] = CustomUser.objects.count()
        
        # Départs à venir (7 prochains jours) avec statistiques
        end_date = today + timedelta(days=7)
        upcoming_departures = Departure.objects.select_related(
            'trip', 'bus'
        ).prefetch_related(
            'reservation_set'
        ).filter(
            date__gte=today,
            date__lte=end_date,
        ).order_by('date', 'time')

        # Organiser les départs par date
        departures_by_date = {}
        for departure in upcoming_departures:
            date_str = departure.date.strftime('%Y-%m-%d')
            if date_str not in departures_by_date:
                departures_by_date[date_str] = []
            
            # Utiliser une seule requête pour compter les réservations actives
            reservations_count = departure.reservation_set.all().filter(
                status__in=['P', 'C']
            ).count()
            
            bus_capacity = departure.bus.capacity
            available_seats = max(0, bus_capacity - reservations_count)
            occupancy_rate = (reservations_count / bus_capacity * 100) if bus_capacity > 0 else 0
              # Ajouter les informations enrichies
            departure_info = {
                'departure': departure,
                'reservations_count': reservations_count,
                'available_seats': available_seats,
                'occupancy_rate': min(100, occupancy_rate)  # Plafonner à 100%
            }
            departures_by_date[date_str].append(departure_info)
            
        context['departures_by_date'] = departures_by_date
        context['upcoming_trips'] = upcoming_departures.count()
        context['date_range'] = [today + timedelta(days=x) for x in range(8)]
        
        # Réservations récentes (10 dernières)
        recent_reservations = Reservation.objects.select_related(
            'user',
            'departure__trip',
            'departure__bus'
        ).filter(
            status__in=['P', 'C']  # Uniquement les réservations actives
        ).order_by('-booked_at')[:10]
        context['recent_reservations'] = recent_reservations

        # Messages récents (5 derniers sans réponse)
        recent_messages = ContactMessage.objects.filter(
            replied_at__isnull=True
        ).order_by('-submitted_at')[:5]
        context['recent_messages'] = recent_messages

        return context

def user_list(request):
    # Logique pour afficher la liste des utilisateurs
    return render(request, 'gareci_admin/user_list.html')