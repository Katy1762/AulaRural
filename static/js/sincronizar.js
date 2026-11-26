// Envía al servidor la asistencia guardada sin conexión y la quita de la cola local
(function () {
  const NOMBRE_BD = 'aularural';
  const VERSION_BD = 1;
  let enCurso = false;

  // Abre la base local y crea los almacenes si no existen
  function abrirBD() {
    return new Promise((resolver, rechazar) => {
      const peticion = indexedDB.open(NOMBRE_BD, VERSION_BD);
      peticion.onupgradeneeded = () => {
        const bd = peticion.result;
        bd.createObjectStore('grupos', { keyPath: 'id' });
        bd.createObjectStore('cola', { keyPath: 'uuid' });
        bd.createObjectStore('meta', { keyPath: 'clave' });
      };
      peticion.onsuccess = () => resolver(peticion.result);
      peticion.onerror = () => rechazar(peticion.error);
    });
  }

  // Lee todos los registros pendientes
  async function leerCola() {
    const bd = await abrirBD();
    return new Promise((resolver, rechazar) => {
      const peticion = bd.transaction('cola').objectStore('cola').getAll();
      peticion.onsuccess = () => resolver(peticion.result);
      peticion.onerror = () => rechazar(peticion.error);
    });
  }

  // Quita de la cola los registros ya procesados por el servidor
  async function borrarDeCola(uuids) {
    const bd = await abrirBD();
    return new Promise((resolver, rechazar) => {
      const tx = bd.transaction('cola', 'readwrite');
      uuids.forEach((u) => tx.objectStore('cola').delete(u));
      tx.oncomplete = () => resolver();
      tx.onerror = () => rechazar(tx.error);
    });
  }

  // Lee una cookie por su nombre (se usa para el token CSRF)
  function leerCookie(nombre) {
    const par = document.cookie.split('; ').find((c) => c.startsWith(nombre + '='));
    return par ? decodeURIComponent(par.split('=')[1]) : '';
  }

  // Muestra un mensaje en todos los lugares de estado de la página
  function avisar(texto) {
    document.querySelectorAll('[data-estado-sync]').forEach((el) => { el.textContent = texto; });
  }

  async function sincronizar() {
    if (enCurso || !navigator.onLine) return;
    enCurso = true;
    try {
      const cola = await leerCola();
      if (!cola.length) return;
      avisar(`Enviando ${cola.length} registro(s)...`);
      const resp = await fetch('/asistencia/sincronizar/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': leerCookie('csrftoken'),
        },
        body: JSON.stringify({ registros: cola }),
      });
      if (!resp.ok) throw new Error('Respuesta ' + resp.status);
      const resultado = await resp.json();
      const procesados = resultado.guardados.concat(
        resultado.rechazados.map((r) => r.uuid).filter(Boolean)
      );
      await borrarDeCola(procesados);
      let texto = `Enviados al servidor: ${resultado.guardados.length}.`;
      if (resultado.rechazados.length) {
        texto += ` Rechazados por no ser válidos: ${resultado.rechazados.length}.`;
      }
      avisar(texto);
      document.dispatchEvent(new Event('cola-actualizada'));
    } catch (e) {
      avisar('No se pudo enviar. Se intentará de nuevo cuando haya conexión y sesión iniciada.');
    } finally {
      enCurso = false;
    }
  }

  window.addEventListener('online', sincronizar);
  document.addEventListener('DOMContentLoaded', sincronizar);
})();