import pytest


# Prueba de humo: confirma que pytest, Django y MySQL funcionan juntos
@pytest.mark.django_db
def test_login_responde(client):
    respuesta = client.get('/login/')
    assert respuesta.status_code == 200

    

# El panel carga para un docente con sesión iniciada
def test_panel_carga(cliente_docente):
    respuesta = cliente_docente.get('/')
    assert respuesta.status_code == 200
    assert 'Actividad reciente' in respuesta.content.decode()