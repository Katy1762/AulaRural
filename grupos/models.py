from django.conf import settings
from django.db import models


class Grupo(models.Model):
    """Un curso del docente, por ejemplo: 5.º A del año 2026."""
    # Cada grupo pertenece a un docente (usuario)
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grupos'
    )
    nombre = models.CharField('nombre', max_length=60)
    grado = models.CharField('grado', max_length=30)
    anio = models.PositiveSmallIntegerField('año')

    class Meta:
        ordering = ['grado', 'nombre']
        # Regla: un docente no puede repetir el mismo grupo en el mismo año
        constraints = [
            models.UniqueConstraint(
                fields=['docente', 'nombre', 'anio'],
                name='grupo_unico_por_docente_y_anio',
            )
        ]

    def __str__(self):
        return f'{self.nombre} ({self.anio})'


class Estudiante(models.Model):
    """Un estudiante que pertenece a un grupo."""
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='estudiantes')
    nombres = models.CharField('nombres', max_length=80)
    apellidos = models.CharField('apellidos', max_length=80)
    codigo = models.CharField('código', max_length=30)

    class Meta:
        ordering = ['apellidos', 'nombres']
        # Regla: el código no se repite dentro del mismo grupo
        constraints = [
            models.UniqueConstraint(
                fields=['grupo', 'codigo'],
                name='estudiante_codigo_unico_por_grupo',
            )
        ]

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'