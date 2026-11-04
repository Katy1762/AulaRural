from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Asignatura(models.Model):
    """Materia que se enseña, por ejemplo: Matemáticas."""
    nombre = models.CharField('nombre', max_length=80, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Planeacion(models.Model):
    """Planeación semanal de clase de un docente (entidad principal del CRUD)."""
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planeaciones'
    )
    # PROTECT: no deja borrar una asignatura que tenga planeaciones
    asignatura = models.ForeignKey(
        Asignatura, on_delete=models.PROTECT, related_name='planeaciones'
    )
    grado = models.CharField('grado', max_length=30)
    # La semana debe estar entre 1 y 52
    semana = models.PositiveSmallIntegerField(
        'semana', validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    objetivos = models.TextField('objetivos')
    temas = models.TextField('temas')
    actividades = models.TextField('actividades')
    recursos = models.TextField('recursos', blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creada']
        verbose_name = 'planeación'
        verbose_name_plural = 'planeaciones'

    def __str__(self):
        return f'{self.asignatura} · {self.grado} · semana {self.semana}'