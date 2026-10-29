from django.urls import path
from . import views

urlpatterns = [
    # '' significa /grupos/ (el prefijo lo pone aularural/urls.py)
    path('', views.inicio, name='grupos'),
]