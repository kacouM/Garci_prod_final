
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Formulaire de création d'un nouvel utilisateur."""
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # on demande au minimum le nom et l'email

class CustomUserChangeForm(UserChangeForm):
    """Formulaire de modification de l'utilisateur."""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_active', 'is_staff']
