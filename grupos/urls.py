from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='grupos'),
    path('nuevo/', views.crear, name='grupo_crear'),
    path('<int:pk>/', views.detalle, name='grupo_detalle'),
    path('<int:pk>/editar/', views.editar, name='grupo_editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='grupo_eliminar'),
    path('<int:grupo_pk>/estudiantes/nuevo/', views.estudiante_crear, name='estudiante_crear'),
    path('estudiantes/<int:pk>/editar/', views.estudiante_editar, name='estudiante_editar'),
    path('estudiantes/<int:pk>/eliminar/', views.estudiante_eliminar, name='estudiante_eliminar'),
]