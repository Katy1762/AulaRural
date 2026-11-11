from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cuentas.permisos import es_directivo, solo_docente

from .forms import PlaneacionForm
from .models import Asignatura, Planeacion


def _propias(request):
    """Solo las planeaciones del docente que inició sesión."""
    return Planeacion.objects.filter(docente=request.user).select_related('asignatura')


def _visibles(request):
    """El directivo ve todas (solo lectura); el docente, solo las suyas."""
    if es_directivo(request.user):
        return Planeacion.objects.select_related('asignatura', 'docente').all()
    return _propias(request)


@login_required
def lista(request):
    # CONSULTAR: listado con filtros opcionales
    planeaciones = _visibles(request)
    asignatura = request.GET.get('asignatura', '')
    grado = request.GET.get('grado', '').strip()
    semana = request.GET.get('semana', '').strip()
    if asignatura:
        planeaciones = planeaciones.filter(asignatura_id=asignatura)
    if grado:
        planeaciones = planeaciones.filter(grado__icontains=grado)
    if semana.isdigit():
        planeaciones = planeaciones.filter(semana=semana)
    return render(request, 'planeaciones/lista.html', {
        'planeaciones': planeaciones,
        'asignaturas': Asignatura.objects.all(),
        'filtro_asignatura': asignatura,
        'filtro_grado': grado,
        'filtro_semana': semana,
    })


@login_required
def detalle(request, pk):
    # El directivo puede ver cualquiera; el docente, solo las suyas
    planeacion = get_object_or_404(_visibles(request), pk=pk)
    return render(request, 'planeaciones/detalle.html', {'planeacion': planeacion})


@login_required
@solo_docente
def crear(request):
    # CREAR
    if request.method == 'POST':
        form = PlaneacionForm(request.POST, docente=request.user)
        if form.is_valid():
            planeacion = form.save(commit=False)
            planeacion.docente = request.user  # el docente lo asigna el servidor
            planeacion.save()
            messages.success(request, 'Planeación creada correctamente.')
            return redirect('planeaciones')
    else:
        form = PlaneacionForm(docente=request.user)
    return render(request, 'planeaciones/formulario.html', {
        'form': form, 'titulo': 'Nueva planeación',
    })


@login_required
@solo_docente
def editar(request, pk):
    # EDITAR: solo las propias
    planeacion = get_object_or_404(_propias(request), pk=pk)
    if request.method == 'POST':
        form = PlaneacionForm(request.POST, instance=planeacion, docente=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planeación actualizada correctamente.')
            return redirect('planeacion_detalle', pk=planeacion.pk)
    else:
        form = PlaneacionForm(instance=planeacion, docente=request.user)
    return render(request, 'planeaciones/formulario.html', {
        'form': form, 'titulo': 'Editar planeación',
    })


@login_required
@solo_docente
def eliminar(request, pk):
    # ELIMINAR: primero pide confirmación (GET) y borra solo con POST
    planeacion = get_object_or_404(_propias(request), pk=pk)
    if request.method == 'POST':
        planeacion.delete()
        messages.success(request, 'Planeación eliminada.')
        return redirect('planeaciones')
    return render(request, 'planeaciones/confirmar_eliminar.html', {
        'planeacion': planeacion,
    })