from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='informes'),
    path('<int:grupo_pk>/', views.informe, name='informe_grupo'),
]