from django.urls import path
from . import views

urlpatterns = [
    # '' significa /planeaciones/
    path('', views.inicio, name='planeaciones'),
]