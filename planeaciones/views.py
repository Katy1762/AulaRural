from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Pantalla provisional del módulo Planeaciones (aquí irá el CRUD principal)
@login_required  # solo usuarios con sesión iniciada
def inicio(request):
    return render(request, 'proximamente.html', {
        'titulo': 'Planeaciones',
        'descripcion': 'Aquí podrás crear y consultar tus planeaciones de clase.',
    })