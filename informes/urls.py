from django.urls import path
from . import views

urlpatterns = [
    # '' significa /informes/
    path('', views.inicio, name='informes'),
]