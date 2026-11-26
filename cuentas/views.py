from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render
from django.utils import timezone

from asistencia.models import Asistencia
from cuentas.permisos import es_directivo
from grupos.models import Grupo
from planeaciones.models import Planeacion


# Vista del panel principal.
# @login_required obliga a iniciar sesión: si no, redirige al login.
@login_required
def panel(request):
    # El directivo ve todo; el docente, solo lo suyo
    if es_directivo(request.user):
        grupos = Grupo.objects.all()
        planeaciones = Planeacion.objects.all()
    else:
        grupos = Grupo.objects.filter(docente=request.user)
        planeaciones = Planeacion.objects.filter(docente=request.user)

    # Porcentaje de asistencia de los últimos 30 días (la tardanza cuenta como asistencia)
    desde = timezone.localdate() - timedelta(days=30)
    registros = Asistencia.objects.filter(estudiante__grupo__in=grupos, fecha__gte=desde)
    total = registros.count()
    porcentaje = None
    if total:
        presentes = registros.exclude(estado=Asistencia.AUSENTE).count()
        porcentaje = round(presentes * 100 / total)

    # Actividad reciente: últimas asistencias guardadas y planeaciones editadas
    actividad = []
    sesiones = (
        Asistencia.objects.filter(estudiante__grupo__in=grupos)
        .values('estudiante__grupo__nombre', 'fecha')
        .annotate(cuando=Max('actualizada'))
        .order_by('-cuando')[:5]
    )
    for s in sesiones:
        actividad.append({
            'texto': f"Asistencia registrada en {s['estudiante__grupo__nombre']}",
            'cuando': s['cuando'],
        })
    for p in planeaciones.select_related('asignatura').order_by('-actualizada')[:5]:
        actividad.append({
            'texto': f'Planeación de {p.asignatura} guardada ({p.grado})',
            'cuando': p.actualizada,
        })
    actividad.sort(key=lambda a: a['cuando'], reverse=True)

    # Muestra la plantilla panel.html con las tarjetas de los módulos
    return render(request, 'panel.html', {
        'porcentaje': porcentaje,
        'actividad': actividad[:6],
    })