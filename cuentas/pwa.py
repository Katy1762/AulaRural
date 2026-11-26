from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static

# Versión de la caché: sube el número cuando cambies los archivos que guarda el service worker
VERSION_CACHE = 'v3'

# Manifiesto: describe la app para poder instalarla en el celular
def manifiesto(request):
    datos = {
        'name': 'AulaRural',
        'short_name': 'AulaRural',
        'description': 'Organiza tu trabajo docente: grupos, planeaciones y asistencia.',
        'lang': 'es-CO',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#FAF7F0',
        'theme_color': '#2F6B4F',
        'icons': [
            {'src': static('img/icon-192.png'), 'sizes': '192x192', 'type': 'image/png'},
            {'src': static('img/icon-512.png'), 'sizes': '512x512', 'type': 'image/png'},
            {'src': static('img/icon-maskable-512.png'), 'sizes': '512x512',
             'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    return JsonResponse(datos, content_type='application/manifest+json')


# El service worker se sirve desde la raíz para poder controlar todo el sitio
def service_worker(request):
    respuesta = render(request, 'pwa/sw.js', {'version': VERSION_CACHE},
                       content_type='application/javascript')
    respuesta['Service-Worker-Allowed'] = '/'
    # El navegador debe revisar siempre si hay una versión nueva
    respuesta['Cache-Control'] = 'no-cache'
    return respuesta


# Página pública que se muestra cuando no hay internet
def sin_conexion(request):
    return render(request, 'pwa/sin_conexion.html')