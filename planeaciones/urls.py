from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista, name='planeaciones'),
    path('nueva/', views.crear, name='planeacion_crear'),
    path('<int:pk>/', views.detalle, name='planeacion_detalle'),
    path('<int:pk>/editar/', views.editar, name='planeacion_editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='planeacion_eliminar'),
]