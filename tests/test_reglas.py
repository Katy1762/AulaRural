from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from asistencia.models import Asistencia
from grupos.models import Grupo
from planeaciones.models import Planeacion


# Extra: en el informe la tardanza cuenta como asistencia
def test_informe_cuenta_tardanza_como_asistencia(cliente_docente, docente, grupo):
    estudiante = grupo.estudiantes.first()
    hoy = timezone.localdate()

    # Un asistió, una tardanza y una ausencia: (1 + 1) / 3 = 67 %
    for dias, estado in [(0, 'asistio'), (1, 'tardanza'), (2, 'ausente')]:
        Asistencia.objects.create(
            estudiante=estudiante, fecha=hoy - timedelta(days=dias),
            estado=estado, registrado_por=docente,
        )

    respuesta = cliente_docente.get(reverse('informe_grupo', args=[grupo.pk]))
    fila = next(f for f in respuesta.context['filas'] if f['estudiante'].pk == estudiante.pk)
    assert fila['total'] == 3
    assert fila['porcentaje'] == 67


# Extra: eliminar un grupo exige confirmar con POST
def test_eliminar_grupo_requiere_confirmacion(cliente_docente, grupo):
    url = reverse('grupo_eliminar', args=[grupo.pk])

    # Con GET solo muestra la confirmación y no borra nada
    assert cliente_docente.get(url).status_code == 200
    assert Grupo.objects.filter(pk=grupo.pk).exists()

    # Con POST sí lo elimina
    assert cliente_docente.post(url).status_code == 302
    assert not Grupo.objects.filter(pk=grupo.pk).exists()


# Extra: un docente no puede editar la planeación de otro
def test_docente_no_edita_planeacion_ajena(cliente_docente, otro_docente, asignatura):
    ajena = Planeacion.objects.create(
        docente=otro_docente, asignatura=asignatura, grado='6°', semana=4,
        objetivos='Comprender el ciclo del agua en la naturaleza.',
        temas='Ciclo del agua', actividades='Experimento en clase',
    )
    respuesta = cliente_docente.get(reverse('planeacion_editar', args=[ajena.pk]))
    assert respuesta.status_code == 404