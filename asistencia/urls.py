from django.urls import path
from . import views

urlpatterns = [
    # '' significa /asistencia/
    path('', views.inicio, name='asistencia'),
]