"""Configuración de Django para AulaRural."""

from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Lee las variables del archivo .env (no se sube a GitHub)
load_dotenv(BASE_DIR / '.env')


# Convierte una variable de entorno en verdadero o falso
def env_bool(nombre, defecto=False):
    valor = os.environ.get(nombre)
    if valor is None:
        return defecto
    return valor.strip().lower() in ('1', 'true', 'si', 'sí', 'yes')


# Convierte "a,b,c" en una lista
def env_lista(nombre, defecto=''):
    return [x.strip() for x in os.environ.get(nombre, defecto).split(',') if x.strip()]


# Apagado por defecto: solo se enciende en el .env de desarrollo
DEBUG = env_bool('DEBUG', False)

# La clave secreta nunca va en el código; sin ella la app no arranca
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Falta SECRET_KEY: agrégala al archivo .env.')

# Direcciones desde las que se permite servir la app
ALLOWED_HOSTS = env_lista('ALLOWED_HOSTS', '127.0.0.1,localhost')

# Orígenes de confianza para formularios en HTTPS, por ejemplo https://usuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS = env_lista('CSRF_TRUSTED_ORIGINS')

# Seguridad en producción: se activa desde el .env del servidor
COOKIES_SEGURAS = env_bool('COOKIES_SEGURAS', False)
SESSION_COOKIE_SECURE = COOKIES_SEGURAS
CSRF_COOKIE_SECURE = COOKIES_SEGURAS

FORZAR_HTTPS = env_bool('FORZAR_HTTPS', False)
SECURE_SSL_REDIRECT = FORZAR_HTTPS
SECURE_HSTS_SECONDS = 3600 if FORZAR_HTTPS else 0
# Avisos aceptados: HSTS con subdominios y preload no aplican a una dirección
# compartida (usuario.pythonanywhere.com), porque el dominio base no es nuestro.
# Si más adelante se usa un dominio propio, hay que revisarlos.
SILENCED_SYSTEM_CHECKS = ['security.W005', 'security.W021']

# Apps instaladas: las seis primeras vienen con Django, las demás son los módulos del proyecto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuentas',        # login, roles y panel principal
    'grupos',         # grupos y estudiantes
    'planeaciones',   # planeaciones académicas
    'asistencia',     # registro de asistencia
    'informes',       # resúmenes de asistencia
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aularural.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Carpeta global donde Django busca base.html, panel.html, 403.html, etc.
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aularural.wsgi.application'


# Base de datos MySQL; las credenciales vienen de variables de entorno
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Idioma y zona horaria de Colombia
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# Archivos estáticos: collectstatic los reúne en STATIC_ROOT para el servidor
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'panel'
LOGOUT_REDIRECT_URL = 'login'