{% load static %}
// Service worker de AulaRural. Versión de caché: {{ version }}
const CACHE = 'aularural-{{ version }}';

// Archivos que se guardan al instalar para que la app abra sin internet
const BASICOS = [
  '/sin-conexion/',
  '{% static "css/estilos.css" %}',
  '{% static "img/icon-192.png" %}',
];

// Instalación: guarda los archivos básicos
self.addEventListener('install', (evento) => {
  evento.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(BASICOS))
      .then(() => self.skipWaiting())
  );
});

// Activación: borra las cachés de versiones anteriores
self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys()
      .then((nombres) => Promise.all(
        nombres.filter((n) => n !== CACHE).map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (evento) => {
  const peticion = evento.request;

  // Solo se interceptan lecturas; los formularios (POST) siempre van a la red
  if (peticion.method !== 'GET') return;

  const url = new URL(peticion.url);
  if (url.origin !== self.location.origin) return;

  // Archivos estáticos: primero la caché y se actualiza en segundo plano
  if (url.pathname.startsWith('/static/')) {
    evento.respondWith(
      caches.open(CACHE).then((cache) =>
        cache.match(peticion).then((guardado) => {
          const actualizado = fetch(peticion)
            .then((resp) => {
              if (resp.ok) cache.put(peticion, resp.clone());
              return resp;
            })
            .catch(() => guardado);
          return guardado || actualizado;
        })
      )
    );
    return;
  }

  // Páginas: siempre de la red. Las páginas con datos personales no se guardan.
  // Sin internet se muestra la página de aviso.
  if (peticion.mode === 'navigate') {
    evento.respondWith(
      fetch(peticion).catch(() => caches.match('/sin-conexion/'))
    );
  }
});