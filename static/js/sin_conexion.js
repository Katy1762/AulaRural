// Guarda los grupos y estudiantes del docente en el navegador (IndexedDB)
const NOMBRE_BD = 'aularural';
const VERSION_BD = 1;

// Abre la base local y crea los almacenes la primera vez
function abrirBD() {
  return new Promise((resolver, rechazar) => {
    const peticion = indexedDB.open(NOMBRE_BD, VERSION_BD);
    peticion.onupgradeneeded = () => {
      const bd = peticion.result;
      bd.createObjectStore('grupos', { keyPath: 'id' });
      // La cola guardará la asistencia pendiente de enviar (paso 3)
      bd.createObjectStore('cola', { keyPath: 'uuid' });
      bd.createObjectStore('meta', { keyPath: 'clave' });
    };
    peticion.onsuccess = () => resolver(peticion.result);
    peticion.onerror = () => rechazar(peticion.error);
  });
}

// Reemplaza los grupos guardados por los recibidos y anota la fecha
async function guardarGrupos(grupos) {
  const bd = await abrirBD();
  return new Promise((resolver, rechazar) => {
    const tx = bd.transaction(['grupos', 'meta'], 'readwrite');
    tx.objectStore('grupos').clear();
    grupos.forEach((g) => tx.objectStore('grupos').put(g));
    tx.objectStore('meta').put({
      clave: 'preparado',
      fecha: new Date().toISOString(),
      total: grupos.length,
    });
    tx.oncomplete = () => resolver();
    tx.onerror = () => rechazar(tx.error);
  });
}

// Lee cuándo fue la última preparación (o null si nunca)
async function leerPreparacion() {
  const bd = await abrirBD();
  return new Promise((resolver, rechazar) => {
    const peticion = bd.transaction('meta').objectStore('meta').get('preparado');
    peticion.onsuccess = () => resolver(peticion.result || null);
    peticion.onerror = () => rechazar(peticion.error);
  });
}

// Muestra el estado debajo del botón
function mostrarEstado(elemento, meta) {
  if (!meta) {
    elemento.textContent = 'Todavía no has preparado este equipo.';
    return;
  }
  const cuando = new Date(meta.fecha).toLocaleString('es-CO');
  elemento.textContent = `Listo: ${meta.total} grupo(s) guardados el ${cuando}`;
}

document.addEventListener('DOMContentLoaded', async () => {
  const boton = document.getElementById('btn-preparar');
  const estado = document.getElementById('estado-preparar');
  if (!boton || !estado) return;

  // Al abrir la página, muestra si ya se preparó antes
  try {
    mostrarEstado(estado, await leerPreparacion());
  } catch (e) {
    estado.textContent = 'Este navegador no permite guardar datos para uso sin conexión.';
    boton.disabled = true;
    return;
  }

  boton.addEventListener('click', async () => {
    boton.disabled = true;
    estado.textContent = 'Preparando...';
    try {
      const resp = await fetch('/asistencia/datos-sin-conexion/', { credentials: 'same-origin' });
      if (!resp.ok) throw new Error('Respuesta ' + resp.status);
      const datos = await resp.json();
      await guardarGrupos(datos.grupos);
      mostrarEstado(estado, await leerPreparacion());
    } catch (e) {
      estado.textContent = 'No se pudo preparar. Revisa tu conexión e inténtalo de nuevo.';
    } finally {
      boton.disabled = false;
    }
  });
});