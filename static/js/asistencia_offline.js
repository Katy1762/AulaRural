// Pantalla de asistencia sin conexión: lee los grupos guardados y deja los registros en una cola local
const NOMBRE_BD = 'aularural';
const VERSION_BD = 1;
const ESTADOS = [
  ['asistio', 'Asistió'],
  ['ausente', 'Ausente'],
  ['tardanza', 'Tardanza'],
];

let grupos = [];
const el = (id) => document.getElementById(id);

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

// Lee todos los registros de un almacén
async function leerTodo(almacen) {
  const bd = await abrirBD();
  return new Promise((resolver, rechazar) => {
    const peticion = bd.transaction(almacen).objectStore(almacen).getAll();
    peticion.onsuccess = () => resolver(peticion.result);
    peticion.onerror = () => rechazar(peticion.error);
  });
}

// Guarda varios registros en la cola en una sola transacción
async function guardarEnCola(registros) {
  const bd = await abrirBD();
  return new Promise((resolver, rechazar) => {
    const tx = bd.transaction('cola', 'readwrite');
    registros.forEach((r) => tx.objectStore('cola').put(r));
    tx.oncomplete = () => resolver();
    tx.onerror = () => rechazar(tx.error);
  });
}

// Fecha de hoy en hora local, con formato AAAA-MM-DD
function hoyLocal() {
  const d = new Date();
  const mes = String(d.getMonth() + 1).padStart(2, '0');
  const dia = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mes}-${dia}`;
}

// Indica si el navegador tiene conexión
function mostrarConexion() {
  el('conexion').textContent = navigator.onLine
    ? 'Hay conexión. También puedes usar la pantalla normal de Asistencia.'
    : 'Sin conexión: lo que guardes quedará en este equipo hasta que vuelva el internet.';
}

// Muestra cuántos registros esperan ser enviados
async function mostrarPendientes() {
  const cola = await leerTodo('cola');
  el('pendientes').textContent = cola.length
    ? `Registros pendientes de enviar: ${cola.length}`
    : 'No hay registros pendientes.';
}

// Dibuja la tabla de estudiantes del grupo y la fecha elegidos
async function dibujarTabla() {
  const cuerpo = el('cuerpo-tabla');
  cuerpo.replaceChildren();
  const grupo = grupos.find((g) => String(g.id) === el('grupo').value);
  if (!grupo) return;

  // Si ya hay algo en la cola para esa fecha, se muestra marcado
  const cola = await leerTodo('cola');
  const marcados = {};
  cola.filter((r) => r.fecha === el('fecha').value)
      .forEach((r) => { marcados[r.estudiante] = r.estado; });

  grupo.estudiantes.forEach((e) => {
    const fila = document.createElement('tr');
    const celdaNombre = document.createElement('td');
    celdaNombre.textContent = `${e.apellidos} ${e.nombres}`;
    const celdaEstado = document.createElement('td');
    const opciones = document.createElement('div');
    opciones.className = 'opciones-asistencia';
    ESTADOS.forEach(([valor, etiqueta]) => {
      const label = document.createElement('label');
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = `estado_${e.id}`;
      radio.value = valor;
      radio.checked = (marcados[e.id] || 'asistio') === valor;
      label.append(radio, ' ' + etiqueta);
      opciones.append(label);
    });
    celdaEstado.append(opciones);
    fila.append(celdaNombre, celdaEstado);
    cuerpo.append(fila);
  });
}

// Guarda en la cola un registro por estudiante, cada uno con su uuid
async function guardar() {
  const mensaje = el('mensaje');
  const grupo = grupos.find((g) => String(g.id) === el('grupo').value);
  const fecha = el('fecha').value;
  if (!grupo) return;
  if (!fecha || fecha > hoyLocal()) {
    mensaje.textContent = 'Elige una fecha que no sea futura.';
    return;
  }
  try {
    // Si el estudiante ya tenía un registro pendiente ese día, se reutiliza su uuid
    const cola = await leerTodo('cola');
    const existentes = {};
    cola.forEach((r) => { existentes[`${r.estudiante}|${r.fecha}`] = r.uuid; });
    const registros = grupo.estudiantes.map((e) => {
      const marcado = document.querySelector(`input[name="estado_${e.id}"]:checked`);
      return {
        uuid: existentes[`${e.id}|${fecha}`] || crypto.randomUUID(),
        grupo: grupo.id,
        estudiante: e.id,
        fecha,
        estado: marcado ? marcado.value : 'asistio',
        creado: new Date().toISOString(),
      };
    });
    await guardarEnCola(registros);
    mensaje.textContent = `Guardado en este equipo: ${registros.length} registro(s).`;
    await mostrarPendientes();
  } catch (e) {
    mensaje.textContent = 'No se pudo guardar en este equipo.';
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  mostrarConexion();
    // Cuando se envía la cola, se actualizan los pendientes y la tabla
  document.addEventListener('cola-actualizada', () => { mostrarPendientes(); dibujarTabla(); });
  window.addEventListener('online', mostrarConexion);
  window.addEventListener('offline', mostrarConexion);

  try {
    grupos = await leerTodo('grupos');
  } catch (e) {
    grupos = [];
  }
  if (!grupos.length) {
    el('aviso-vacio').hidden = false;
    return;
  }

  // Llena el selector de grupos y deja la fecha de hoy
  grupos.forEach((g) => {
    const opcion = document.createElement('option');
    opcion.value = g.id;
    opcion.textContent = `${g.nombre} (${g.grado})`;
    el('grupo').append(opcion);
  });
  el('fecha').value = hoyLocal();
  el('fecha').max = hoyLocal();
  el('captura').hidden = false;

  el('grupo').addEventListener('change', dibujarTabla);
  el('fecha').addEventListener('change', dibujarTabla);
  el('btn-guardar').addEventListener('click', guardar);
  await dibujarTabla();
  await mostrarPendientes();
});