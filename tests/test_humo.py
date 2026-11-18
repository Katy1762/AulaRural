import pytest


# Prueba de humo: confirma que pytest, Django y MySQL funcionan juntos
@pytest.mark.django_db
def test_login_responde(client):
    respuesta = client.get('/login/')
    assert respuesta.status_code == 200