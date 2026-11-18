from django.urls import reverse

from planeaciones.models import Planeacion


# Caso 1 (positivo): un docente crea una planeación válida
def test_docente_crea_planeacion_valida(cliente_docente, datos_planeacion):
    respuesta = cliente_docente.post(reverse('planeacion_crear'), datos_planeacion)

    # Redirige al listado y la planeación queda guardada
    assert respuesta.status_code == 302
    assert Planeacion.objects.count() == 1

    # Aparece en el listado del docente
    listado = cliente_docente.get(reverse('planeaciones'))
    assert '4°' in listado.content.decode()


# Caso 2 (negativo): un campo obligatorio vacío es rechazado
def test_planeacion_con_campo_vacio_es_rechazada(cliente_docente, datos_planeacion):
    datos_planeacion['objetivos'] = ''
    respuesta = cliente_docente.post(reverse('planeacion_crear'), datos_planeacion)

    # Vuelve al formulario con el error y no guarda nada
    assert respuesta.status_code == 200
    assert 'objetivos' in respuesta.context['form'].errors
    assert Planeacion.objects.count() == 0


# Extra: los objetivos con menos de 10 caracteres son rechazados
def test_objetivos_muy_cortos_son_rechazados(cliente_docente, datos_planeacion):
    datos_planeacion['objetivos'] = 'Corto'
    respuesta = cliente_docente.post(reverse('planeacion_crear'), datos_planeacion)

    assert respuesta.status_code == 200
    assert 'objetivos' in respuesta.context['form'].errors
    assert Planeacion.objects.count() == 0


# Extra: no se repite asignatura, grado y semana para el mismo docente
def test_planeacion_repetida_es_rechazada(cliente_docente, planeacion, datos_planeacion):
    # Mismos datos de la planeación que ya existe (5°, semana 2)
    datos_planeacion['grado'] = planeacion.grado
    datos_planeacion['semana'] = planeacion.semana
    respuesta = cliente_docente.post(reverse('planeacion_crear'), datos_planeacion)

    assert respuesta.status_code == 200
    assert respuesta.context['form'].non_field_errors()
    assert Planeacion.objects.count() == 1