from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='asistencia'),
    # Datos del docente para usar sin conexión
    path('datos-sin-conexion/', views.datos_sin_conexion, name='asistencia_datos_sin_conexion'),
    path('<int:grupo_pk>/', views.tomar, name='asistencia_tomar'),
]