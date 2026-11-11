from django.conf import settings
from django.db import models


class Perfil(models.Model):
    DOCENTE = 'docente'
    DIRECTIVO = 'directivo'
    ROLES = [(DOCENTE, 'Docente'), (DIRECTIVO, 'Directivo')]

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField('rol', max_length=20, choices=ROLES, default=DOCENTE)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'