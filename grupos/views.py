from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Pantalla provisional del módulo Grupos (se completará en la Clase 2)
@login_required  # solo usuarios con sesión iniciada
def inicio(request):
    # Enviamos título y descripción a la plantilla como datos (contexto)
    return render(request, 'proximamente.html', {
        'titulo': 'Grupos',
        'descripcion': 'Aquí podrás crear tus grupos y registrar a tus estudiantes.',
    })