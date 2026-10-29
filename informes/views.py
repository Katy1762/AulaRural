from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Pantalla provisional del módulo Informes
@login_required  # solo usuarios con sesión iniciada
def inicio(request):
    return render(request, 'proximamente.html', {
        'titulo': 'Informes',
        'descripcion': 'Aquí verás el resumen de asistencia de cada grupo.',
    })