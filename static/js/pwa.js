// Registra el service worker si el navegador lo soporta
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .catch((error) => console.error('No se pudo registrar el service worker:', error));
  });
}