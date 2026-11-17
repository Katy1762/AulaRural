from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cuentas.permisos import es_directivo, solo_docente

from .forms import EstudianteForm, GrupoForm
from .models import Estudiante, Grupo


# Grupos del docente que inició sesión (para editar y eliminar)
def _propios(request):
    return Grupo.objects.filter(docente=request.user)


# El directivo ve todos los grupos; el docente, solo los suyos
def _visibles(request):
    if es_directivo(request.user):
        return Grupo.objects.select_related('docente').all()
    return _propios(request)


# Estudiantes de los grupos del docente
def _estudiantes_propios(request):
    return Estudiante.objects.filter(grupo__docente=request.user)


# Listado de grupos
@login_required
def lista(request):
    return render(request, 'grupos/lista.html', {'grupos': _visibles(request)})


# Detalle del grupo con sus estudiantes
@login_required
def detalle(request, pk):
    grupo = get_object_or_404(_visibles(request), pk=pk)
    return render(request, 'grupos/detalle.html', {'grupo': grupo, 'estudiantes': grupo.estudiantes.all()})


# Crear grupo: solo docente; el docente lo asigna el servidor
@login_required
@solo_docente
def crear(request):
    form = GrupoForm(request.POST or None, docente=request.user)
    if request.method == 'POST' and form.is_valid():
        grupo = form.save(commit=False)
        grupo.docente = request.user
        grupo.save()
        messages.success(request, 'Grupo creado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/formulario.html', {'form': form, 'titulo': 'Nuevo grupo'})


# Editar grupo: solo docente y solo los propios
@login_required
@solo_docente
def editar(request, pk):
    grupo = get_object_or_404(_propios(request), pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo, docente=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grupo actualizado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/formulario.html', {'form': form, 'titulo': 'Editar grupo'})


# Eliminar grupo: confirma en GET y borra solo con POST
@login_required
@solo_docente
def eliminar(request, pk):
    grupo = get_object_or_404(_propios(request), pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Grupo eliminado.')
        return redirect('grupos')
    return render(request, 'grupos/confirmar_eliminar.html', {'grupo': grupo})


# Agregar estudiante a un grupo propio
@login_required
@solo_docente
def estudiante_crear(request, grupo_pk):
    grupo = get_object_or_404(_propios(request), pk=grupo_pk)
    form = EstudianteForm(request.POST or None, grupo=grupo)
    if request.method == 'POST' and form.is_valid():
        estudiante = form.save(commit=False)
        estudiante.grupo = grupo
        estudiante.save()
        messages.success(request, 'Estudiante agregado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/estudiante_formulario.html',
                  {'form': form, 'grupo': grupo, 'titulo': 'Nuevo estudiante'})


# Editar estudiante de un grupo propio
@login_required
@solo_docente
def estudiante_editar(request, pk):
    estudiante = get_object_or_404(_estudiantes_propios(request), pk=pk)
    form = EstudianteForm(request.POST or None, instance=estudiante, grupo=estudiante.grupo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Estudiante actualizado.')
        return redirect('grupo_detalle', pk=estudiante.grupo.pk)
    return render(request, 'grupos/estudiante_formulario.html',
                  {'form': form, 'grupo': estudiante.grupo, 'titulo': 'Editar estudiante'})


# Eliminar estudiante de un grupo propio
@login_required
@solo_docente
def estudiante_eliminar(request, pk):
    estudiante = get_object_or_404(_estudiantes_propios(request), pk=pk)
    grupo = estudiante.grupo
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/estudiante_confirmar_eliminar.html',
                  {'estudiante': estudiante, 'grupo': grupo})