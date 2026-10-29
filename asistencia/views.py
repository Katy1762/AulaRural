from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Pantalla provisional del módulo Asistencia
@login_required  # solo usuarios con sesión iniciada
def inicio(request):
    return render(request, 'proximamente.html', {
        'titulo': 'Asistencia',
        'descripcion': 'Aquí podrás registrar la asistencia por grupo y fecha.',
    })