# AulaRural

Aplicación web para que los docentes organicen su trabajo académico: grupos y estudiantes, planeaciones de clase, registro de asistencia e informes. Proyecto integrador de Aplicaciones Web II (Uninúñez).

**URL en línea:** [completar al desplegar]

## Funciones

- Inicio y cierre de sesión con dos roles: **Docente** y **Directivo**.
- Grupos y estudiantes: CRUD completo con validaciones.
- Planeaciones por asignatura, grado y semana: CRUD con filtros.
- Asistencia por grupo y fecha (asistió, ausente, tardanza), sin duplicados.
- Informe de asistencia por grupo con conteos, porcentaje y filtro por fechas.

| Función | Docente | Directivo |
| --- | --- | --- |
| Grupos, estudiantes y planeaciones | CRUD de los propios | Solo consulta de todos |
| Asistencia | Registrar y consultar la de sus grupos | Solo consulta |
| Informes | De sus grupos | De todos los grupos |

Los permisos se validan en el servidor: el directivo recibe un 403 si intenta crear, editar o eliminar.

## Tecnologías

Python 3.11, Django 5.2, MySQL 8.0, HTML, CSS y JavaScript. Pruebas con pytest y pytest-django.

## Instalación local (Windows, PowerShell)

1. Clonar el repositorio y entrar a la carpeta:

   ```powershell
   git clone https://github.com/Katy1762/AulaRural.git
   cd AulaRural
   ```

2. Crear y activar el entorno virtual, e instalar las dependencias:

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Crear la base de datos y el usuario en MySQL (reemplaza `TU_CLAVE` por una clave propia):

   ```sql
   CREATE DATABASE aularural CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'aularural_user'@'localhost' IDENTIFIED BY 'TU_CLAVE';
   GRANT ALL PRIVILEGES ON aularural.* TO 'aularural_user'@'localhost';
   GRANT ALL PRIVILEGES ON test_aularural.* TO 'aularural_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Copiar `.env.example` como `.env` y completar los valores. Para generar una `SECRET_KEY`:

   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

5. Crear las tablas. La migración también carga las asignaturas iniciales:

   ```powershell
   python manage.py migrate
   ```

6. Crear un usuario administrador y encender el servidor:

   ```powershell
   python manage.py createsuperuser
   python manage.py runserver
   ```

7. Abrir `http://127.0.0.1:8000/`. Los usuarios docentes se crean en `/admin/`. Para crear un directivo, crear el usuario y, en **Perfiles**, cambiar su rol a *Directivo*.

## Variables de entorno

| Variable | Descripción |
| --- | --- |
| `SECRET_KEY` | Clave secreta de Django. Obligatoria. |
| `DEBUG` | `True` solo en desarrollo. Por defecto `False`. |
| `ALLOWED_HOSTS` | Direcciones permitidas, separadas por comas. |
| `CSRF_TRUSTED_ORIGINS` | Orígenes HTTPS de confianza, por ejemplo la URL en línea. |
| `COOKIES_SEGURAS` | `True` en producción. |
| `FORZAR_HTTPS` | `True` en producción. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Conexión a MySQL. |

El archivo `.env` nunca se sube al repositorio.

## Pruebas

```powershell
pytest -v
```

Hay 14 pruebas automatizadas: planeaciones, permisos, asistencia, informes y persistencia. pytest-django crea una base temporal llamada `test_aularural`, por eso el usuario de MySQL necesita permiso sobre ella (paso 3).

## Estructura

- `cuentas/`: login, roles y panel principal.
- `grupos/`: grupos y estudiantes.
- `planeaciones/`: planeaciones y asignaturas.
- `asistencia/`: registro de asistencia.
- `informes/`: informe de asistencia por grupo.
- `templates/` y `static/`: plantillas y estilos.
- `tests/`: pruebas automatizadas.

## Despliegue

En el servidor se usan las mismas variables de entorno, con `DEBUG=False`, `COOKIES_SEGURAS=True` y `FORZAR_HTTPS=True`. Pasos generales:

1. Clonar el repositorio, crear el entorno virtual e instalar `requirements.txt`.
2. Crear la base de datos MySQL y el archivo `.env` del servidor, con una `SECRET_KEY` distinta a la de desarrollo.
3. `python manage.py migrate`
4. `python manage.py collectstatic`
5. Configurar la aplicación web para que use `aularural.wsgi` y servir la carpeta `staticfiles` en la ruta `/static/`.
6. Crear el usuario administrador y los usuarios de prueba.

## Seguridad y privacidad

- Contraseñas protegidas por Django, protección CSRF y validación en el servidor.
- Claves y datos de conexión fuera del código, en variables de entorno.
- Todos los datos de demostración y de prueba son ficticios; no hay información real de menores.