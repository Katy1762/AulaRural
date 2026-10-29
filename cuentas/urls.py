# Rutas de la app cuentas: inicio de sesión y panel principal
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página de inicio: muestra el panel con las tarjetas
    path('', views.panel, name='panel'),
    # Login y logout usan las vistas que ya trae Django
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]