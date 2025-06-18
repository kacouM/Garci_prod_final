from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

def signup(request):
    """Inscription d'un nouveau client."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # On peut se connecter automatiquement après inscription, ou rediriger vers login
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginRedirectView(LoginView):
    """
    Vue de connexion : redirige automatiquement vers l'accueil (client) ou le dashboard (staff).
    """
    template_name = 'accounts/login.html'
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_success_url(self):
        # Si l'utilisateur est staff, redirige vers le tableau de bord admin
        if self.request.user.is_staff:
            return reverse('dashboard:index')
        # Sinon (client), on renvoie vers la page d'accueil publique
        return reverse('trips:home')

class CustomLogoutView(LogoutView):
    next_page = 'trips:home'  # après déconnexion, retourne à l'accueil public
