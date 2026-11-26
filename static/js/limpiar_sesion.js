// Al pulsar Salir, borra de este equipo los datos guardados para el modo sin conexión
(function () {
  const NOMBRE_BD = 'aularural';
  const VERSION_BD = 1;
  const ALMACENES = ['grupos', 'cola', 'meta'];

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

  // Cuenta los registros que todavía no se han enviado al servidor
  async function contarPendientes() {
    const bd = await abrirBD();
    return new Promise((resolver, rechazar) => {
      const peticion = bd.transaction('cola').objectStore('cola').count();
      peticion.onsuccess = () => { bd.close(); resolver(peticion.result); };
      peticion.onerror = () => rechazar(peticion.error);
    });
  }

  // Vacía todos los almacenes locales (grupos, estudiantes, cola y fecha de preparación)
  async function limpiar() {
    const bd = await abrirBD();
    return new Promise((resolver, rechazar) => {
      const tx = bd.transaction(ALMACENES, 'readwrite');
      ALMACENES.forEach((a) => tx.objectStore(a).clear());
      tx.oncomplete = () => { bd.close(); resolver(); };
      tx.onerror = () => rechazar(tx.error);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('form-salir');
    if (!formulario) return;

    formulario.addEventListener('submit', async (evento) => {
      evento.preventDefault();
      try {
        const pendientes = await contarPendientes();
        if (pendientes > 0) {
          const seguir = window.confirm(
            `Hay ${pendientes} registro(s) de asistencia sin enviar. ` +
            'Si sales ahora se borrarán de este equipo. ¿Salir de todos modos?'
          );
          if (!seguir) return;
        }
        await limpiar();
      } catch (e) {
        // Si no se pudo borrar, igual se cierra la sesión
      }
      formulario.submit();
    });
  });
})();