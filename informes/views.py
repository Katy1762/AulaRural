from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_list_or_404, get_object_or_404, render

from asistencia.models import Asistencia
from cuentas.permisos import es_directivo
from grupos.models import Grupo

#el directivo ve todos los grupos; el docente, solo los suyos 

def _grupos_visibles(request):
    if es_directivo(request.user):
        return Grupo.objects.select_related('docente').all()
    return Grupo.objects.filter(docente=request.user)

# Convierte "2026-11-13" en fecha; si viene vacía o mal escrita, devuelve None
def _leer_fecha(texto):
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError):
        return None


# Lista de grupos para elegir el informe
@login_required
def inicio(request):
    return render(request, 'informes/inicio.html', {'grupos': _grupos_visibles(request)})


# Informe de un grupo, con rango de fechas opcional
@login_required
def informe(request, grupo_pk):
    # 404 si el grupo no existe o no es visible para este usuario
    grupo = get_object_or_404(_grupos_visibles(request), pk=grupo_pk)

    # Fechas del filtro; vienen por GET (?desde=...&hasta=...)
    desde = _leer_fecha(request.GET.get('desde'))
    hasta = _leer_fecha(request.GET.get('hasta'))

    # Q() vacío no filtra nada; se le suman condiciones solo si hay fechas
    filtro = Q()
    if desde:
        filtro &= Q(asistencias__fecha__gte=desde)
    if hasta:
        filtro &= Q(asistencias__fecha__lte=hasta)

    # annotate agrega tres columnas calculadas a cada estudiante.
    # Count con filter cuenta solo los registros de ese estado y de esas fechas,
    # todo en una sola consulta a MySQL.
    estudiantes = grupo.estudiantes.annotate(
        asistio=Count('asistencias', filter=filtro & Q(asistencias__estado=Asistencia.ASISTIO)),
        ausente=Count('asistencias', filter=filtro & Q(asistencias__estado=Asistencia.AUSENTE)),
        tardanza=Count('asistencias', filter=filtro & Q(asistencias__estado=Asistencia.TARDANZA)),
    )

    # Total y porcentaje por estudiante.
    # La tardanza cuenta como asistencia porque el estudiante sí estuvo.
    # Sin registros no hay porcentaje (None), para no dividir por cero.
    filas = []
    for e in estudiantes:
        total = e.asistio + e.ausente + e.tardanza
        porcentaje = round((e.asistio + e.tardanza) * 100 / total) if total else None
        filas.append({'estudiante': e, 'asistio': e.asistio, 'ausente': e.ausente,
                      'tardanza': e.tardanza, 'total': total, 'porcentaje': porcentaje})

    # Resumen del grupo: suma de las columnas de todos los estudiantes
    suma_asistio = sum(f['asistio'] for f in filas)
    suma_ausente = sum(f['ausente'] for f in filas)
    suma_tardanza = sum(f['tardanza'] for f in filas)
    suma_total = suma_asistio + suma_ausente + suma_tardanza

    # Mismo cálculo del porcentaje, pero para todo el grupo
    porcentaje_grupo = round((suma_asistio + suma_tardanza) * 100 / suma_total) if suma_total else None

    return render(request, 'informes/grupo.html', {
        'grupo': grupo,
        'filas': filas,
        'desde': desde,
        'hasta': hasta,
        'resumen': {'asistio': suma_asistio, 'ausente': suma_ausente,
                    'tardanza': suma_tardanza, 'total': suma_total,
                    'porcentaje': porcentaje_grupo},
    }) 

