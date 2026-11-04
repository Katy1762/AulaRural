from django.db import migrations

# Materias que vienen cargadas desde el inicio en cualquier base de datos
ASIGNATURAS = [
    'Matemáticas',
    'Lengua Castellana',
    'Ciencias Naturales',
    'Ciencias Sociales',
    'Inglés',
    'Educación Física',
]


def cargar_asignaturas(apps, schema_editor):
    Asignatura = apps.get_model('planeaciones', 'Asignatura')
    for nombre in ASIGNATURAS:
        # get_or_create evita duplicar las que ya existen
        Asignatura.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ('planeaciones', '0001_initial'),
    ]

    operations = [
        # noop permite deshacer la migración sin borrar datos
        migrations.RunPython(cargar_asignaturas, migrations.RunPython.noop),
    ]