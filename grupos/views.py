from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EstudianteForm, GrupoForm
from .models import Estudiante, Grupo


def _propios(request):
    return Grupo.objects.filter(docente=request.user)


def _estudiantes_propios(request):
    return Estudiante.objects.filter(grupo__docente=request.user)


@login_required
def lista(request):
    grupos = _propios(request)
    return render(request, 'grupos/lista.html', {'grupos': grupos})


@login_required
def detalle(request, pk):
    grupo = get_object_or_404(_propios(request), pk=pk)
    return render(request, 'grupos/detalle.html', {'grupo': grupo, 'estudiantes': grupo.estudiantes.all()})


@login_required
def crear(request):
    form = GrupoForm(request.POST or None, docente=request.user)
    if request.method == 'POST' and form.is_valid():
        grupo = form.save(commit=False)
        grupo.docente = request.user
        grupo.save()
        messages.success(request, 'Grupo creado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/formulario.html', {'form': form, 'titulo': 'Nuevo grupo'})


@login_required
def editar(request, pk):
    grupo = get_object_or_404(_propios(request), pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo, docente=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grupo actualizado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/formulario.html', {'form': form, 'titulo': 'Editar grupo'})


@login_required
def eliminar(request, pk):
    grupo = get_object_or_404(_propios(request), pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Grupo eliminado.')
        return redirect('grupos')
    return render(request, 'grupos/confirmar_eliminar.html', {'grupo': grupo})


@login_required
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


@login_required
def estudiante_editar(request, pk):
    estudiante = get_object_or_404(_estudiantes_propios(request), pk=pk)
    form = EstudianteForm(request.POST or None, instance=estudiante, grupo=estudiante.grupo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Estudiante actualizado.')
        return redirect('grupo_detalle', pk=estudiante.grupo.pk)
    return render(request, 'grupos/estudiante_formulario.html',
                  {'form': form, 'grupo': estudiante.grupo, 'titulo': 'Editar estudiante'})


@login_required
def estudiante_eliminar(request, pk):
    estudiante = get_object_or_404(_estudiantes_propios(request), pk=pk)
    grupo = estudiante.grupo
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado.')
        return redirect('grupo_detalle', pk=grupo.pk)
    return render(request, 'grupos/estudiante_confirmar_eliminar.html',
                  {'estudiante': estudiante, 'grupo': grupo})