
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé. Hérite de AbstractUser (nom d'utilisateur, email, etc.).
    Nous pourrions ajouter des champs ici (par ex. is_client), mais utilisons la version minimale.
    """
    def __str__(self):
        return self.username
