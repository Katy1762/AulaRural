from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='asistencia'),
    path('<int:grupo_pk>/', views.tomar, name='asistencia_tomar'),
]