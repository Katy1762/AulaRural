import uuid

from django.conf import settings
from django.db import models

from grupos.models import Estudiante


class Asistencia(models.Model):
    ASISTIO = 'asistio'
    AUSENTE = 'ausente'
    TARDANZA = 'tardanza'
    ESTADOS = [
        (ASISTIO, 'Asistió'),
        (AUSENTE, 'Ausente'),
        (TARDANZA, 'Tardanza'),
    ]

    uuid = models.UUIDField('identificador', default=uuid.uuid4, unique=True, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField('fecha')
    estado = models.CharField('estado', max_length=10, choices=ESTADOS, default=ASISTIO)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='asistencias_registradas'
    )
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha', 'estudiante__apellidos']
        verbose_name = 'asistencia'
        verbose_name_plural = 'asistencias'
        constraints = [
            models.UniqueConstraint(fields=['estudiante', 'fecha'], name='asistencia_unica_por_estudiante_y_fecha'),
        ]

    def __str__(self):
        return f'{self.estudiante} · {self.fecha} · {self.get_estado_display()}'
    