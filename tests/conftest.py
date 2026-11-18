import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from cuentas.models import Perfil
from grupos.models import Estudiante, Grupo
from planeaciones.models import Asignatura, Planeacion

User = get_user_model()


# Docente de prueba (el perfil se crea solo con la señal)
@pytest.fixture
def docente(db):
    return User.objects.create_user('docente_prueba')


# Otro docente, para probar que no se ven datos ajenos
@pytest.fixture
def otro_docente(db):
    return User.objects.create_user('otro_docente')


# Directivo de prueba: mismo usuario con rol cambiado
@pytest.fixture
def directivo(db):
    usuario = User.objects.create_user('directivo_prueba')
    Perfil.objects.update_or_create(usuario=usuario, defaults={'rol': Perfil.DIRECTIVO})
    return usuario


# Cliente con sesión iniciada, sin usar contraseñas
def _cliente_de(usuario):
    cliente = Client()
    cliente.force_login(usuario)
    return cliente


@pytest.fixture
def cliente_docente(docente):
    return _cliente_de(docente)


@pytest.fixture
def cliente_directivo(directivo):
    return _cliente_de(directivo)


@pytest.fixture
def asignatura(db):
    return Asignatura.objects.get_or_create(nombre='Matemáticas')[0]


# Grupo del docente con dos estudiantes ficticios
@pytest.fixture
def grupo(docente):
    g = Grupo.objects.create(docente=docente, nombre='Grupo Prueba', grado='3°', anio=2026)
    Estudiante.objects.create(grupo=g, nombres='Ana', apellidos='Prueba', codigo='001')
    Estudiante.objects.create(grupo=g, nombres='Luis', apellidos='Ejemplo', codigo='002')
    return g


# Planeación ya guardada del docente
@pytest.fixture
def planeacion(docente, asignatura):
    return Planeacion.objects.create(
        docente=docente, asignatura=asignatura, grado='5°', semana=2,
        objetivos='Reconocer las fracciones en situaciones cotidianas.',
        temas='Fracciones', actividades='Trabajo en parejas',
    )


# Datos válidos para enviar el formulario de planeación
@pytest.fixture
def datos_planeacion(asignatura):
    return {
        'asignatura': asignatura.pk,
        'grado': '4°',
        'semana': 3,
        'objetivos': 'Identificar las partes de una fracción en ejemplos reales.',
        'temas': 'Numerador y denominador',
        'actividades': 'Ejercicios con material concreto',
        'recursos': '',
    }