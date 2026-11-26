from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='asistencia'),
    # Datos del docente para usar sin conexión
    path('datos-sin-conexion/', views.datos_sin_conexion, name='asistencia_datos_sin_conexion'),
    # Pantalla de captura sin conexión
    path('sin-conexion/', views.sin_conexion, name='asistencia_sin_conexion'),
    # Recibe la cola de asistencia guardada sin conexión
    path('sincronizar/', views.sincronizar, name='asistencia_sincronizar'),
    path('<int:grupo_pk>/', views.tomar, name='asistencia_tomar'),
]