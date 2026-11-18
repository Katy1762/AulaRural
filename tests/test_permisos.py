from django.urls import reverse

from grupos.models import Grupo


# Caso 3 (permisos): un directivo no puede editar una planeación
def test_directivo_no_puede_editar_planeacion(cliente_directivo, planeacion):
    url = reverse('planeacion_editar', args=[planeacion.pk])

    # Ni siquiera puede abrir el formulario
    assert cliente_directivo.get(url).status_code == 403

    # Y si envía datos por su cuenta, el servidor también los rechaza
    respuesta = cliente_directivo.post(url, {'grado': 'Modificado'})
    assert respuesta.status_code == 403
    planeacion.refresh_from_db()
    assert planeacion.grado == '5°'


# Caso 4 (permisos): un docente no ve los grupos de otro docente
def test_docente_no_ve_grupos_de_otro(cliente_docente, otro_docente):
    ajeno = Grupo.objects.create(docente=otro_docente, nombre='Grupo Ajeno', grado='1°', anio=2026)

    # No aparece en su listado
    listado = cliente_docente.get(reverse('grupos'))
    assert 'Grupo Ajeno' not in listado.content.decode()

    # Y si escribe la dirección a mano, el servidor responde 404
    assert cliente_docente.get(reverse('grupo_detalle', args=[ajeno.pk])).status_code == 404


# Extra: un directivo no puede crear grupos
def test_directivo_no_puede_crear_grupo(cliente_directivo):
    assert cliente_directivo.get(reverse('grupo_crear')).status_code == 403