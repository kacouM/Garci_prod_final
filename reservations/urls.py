from django.urls import path
from .views import reservation_list, reserve_departure, message_list, delete_message

app_name = 'reservations'
urlpatterns = [
    path('list/', reservation_list, name='list'),
    path('reserve/<int:departure_id>/', reserve_departure, name='reserve'),
    path('messages/', message_list, name='messages'),
    path('messages/delete/<int:pk>/', delete_message, name='delete_message'),
]
