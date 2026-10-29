from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Vista del panel principal.
# @login_required obliga a iniciar sesión: si no, redirige al login.
@login_required
def panel(request):
    # Muestra la plantilla panel.html con las tarjetas de los módulos
    return render(request, 'panel.html')