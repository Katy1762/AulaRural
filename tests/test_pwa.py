# El manifiesto describe la app y trae íconos
def test_manifiesto_describe_la_app(client):
    respuesta = client.get('/manifest.webmanifest')
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos['short_name'] == 'AulaRural'
    assert datos['display'] == 'standalone'
    assert len(datos['icons']) >= 2


# El service worker se sirve como JavaScript y puede controlar todo el sitio
def test_service_worker_controla_todo_el_sitio(client):
    respuesta = client.get('/sw.js')
    assert respuesta.status_code == 200
    assert 'javascript' in respuesta['Content-Type']
    assert respuesta['Service-Worker-Allowed'] == '/'


# La página de aviso es pública: debe abrir aunque no haya sesión
def test_pagina_sin_conexion_es_publica(client):
    assert client.get('/sin-conexion/').status_code == 200