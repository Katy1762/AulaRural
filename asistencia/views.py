from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from cuentas.permisos import es_directivo
from grupos.models import Grupo

from .models import Asistencia


def _grupos_visibles(request):
    if es_directivo(request.user):
        return Grupo.objects.select_related('docente').all()
    return Grupo.objects.filter(docente=request.user)


def _leer_fecha(texto):
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError):
        return timezone.localdate()


@login_required
def inicio(request):
    return render(request, 'asistencia/inicio.html', {
        'grupos': _grupos_visibles(request),
        'hoy': timezone.localdate(),
    })


@login_required
def tomar(request, grupo_pk):
    grupo = get_object_or_404(_grupos_visibles(request), pk=grupo_pk)
    solo_lectura = es_directivo(request.user)
    hoy = timezone.localdate()
    fecha = _leer_fecha(request.POST.get('fecha') or request.GET.get('fecha'))
    estudiantes = list(grupo.estudiantes.all())

    if request.method == 'POST':
        if solo_lectura:
            raise PermissionDenied
        if fecha > hoy:
            messages.error(request, 'No se puede registrar asistencia de una fecha futura.')
        elif not estudiantes:
            messages.error(request, 'Este grupo no tiene estudiantes.')
        else:
            validos = {valor for valor, _ in Asistencia.ESTADOS}
            with transaction.atomic():
                for e in estudiantes:
                    estado = request.POST.get(f'estado_{e.pk}')
                    if estado in validos:
                        Asistencia.objects.update_or_create(
                            estudiante=e, fecha=fecha,
                            defaults={'estado': estado, 'registrado_por': request.user},
                        )
            messages.success(request, 'Asistencia guardada.')
            return redirect(f"{reverse('asistencia_tomar', args=[grupo.pk])}?fecha={fecha.isoformat()}")

    existentes = {
        a.estudiante_id: a.estado
        for a in Asistencia.objects.filter(estudiante__in=estudiantes, fecha=fecha)
    }
    filas = [
        {'estudiante': e, 'estado': existentes.get(e.pk, Asistencia.ASISTIO)}
        for e in estudiantes
    ]
    return render(request, 'asistencia/tomar.html', {
        'grupo': grupo,
        'fecha': fecha,
        'hoy': hoy,
        'filas': filas,
        'estados': Asistencia.ESTADOS,
        'ya_registrada': bool(existentes),
        'solo_lectura': solo_lectura,
    })