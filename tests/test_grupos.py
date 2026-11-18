from django.urls import reverse

from grupos.models import Grupo


# Caso 6 (persistencia): se crea un grupo y luego se consulta
def test_grupo_creado_sigue_almacenado(cliente_docente, docente):
    cliente_docente.post(
        reverse('grupo_crear'),
        {'nombre': 'Grupo Persistente', 'grado': '2°', 'anio': 2026},
    )

    # Se lee de la base de datos, no de memoria
    guardado = Grupo.objects.get(nombre='Grupo Persistente')
    assert guardado.docente == docente

    # Y aparece al volver a consultar el listado
    listado = cliente_docente.get(reverse('grupos'))
    assert 'Grupo Persistente' in listado.content.decode()