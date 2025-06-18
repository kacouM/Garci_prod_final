from django.contrib import admin
from .models import ContactMessage, Reservation

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'replied_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at', 'replied_at')
    readonly_fields = ('submitted_at',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'departure', 'status', 'booked_at')
    search_fields = ('user__username', 'departure__trip__origin', 'departure__trip__destination')
    list_filter = ('status', 'booked_at')
    readonly_fields = ('booked_at',)
