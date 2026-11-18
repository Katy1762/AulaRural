from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from asistencia.models import Asistencia


# Caso 5 (regla de negocio): la asistencia de un estudiante no se duplica en la misma fecha
def test_asistencia_no_se_duplica_en_la_misma_fecha(cliente_docente, grupo):
    estudiante = grupo.estudiantes.first()
    url = reverse('asistencia_tomar', args=[grupo.pk])
    hoy = timezone.localdate().isoformat()

    # Se guarda dos veces la misma fecha, cambiando el estado
    cliente_docente.post(url, {'fecha': hoy, f'estado_{estudiante.pk}': 'ausente'})
    cliente_docente.post(url, {'fecha': hoy, f'estado_{estudiante.pk}': 'asistio'})

    # Queda un solo registro, con el último estado
    registros = Asistencia.objects.filter(estudiante=estudiante, fecha=hoy)
    assert registros.count() == 1
    assert registros.first().estado == 'asistio'


# Extra: el servidor rechaza fechas futuras
def test_asistencia_rechaza_fecha_futura(cliente_docente, grupo):
    estudiante = grupo.estudiantes.first()
    manana = (timezone.localdate() + timedelta(days=1)).isoformat()

    cliente_docente.post(
        reverse('asistencia_tomar', args=[grupo.pk]),
        {'fecha': manana, f'estado_{estudiante.pk}': 'asistio'},
    )
    assert Asistencia.objects.count() == 0