from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import Perfil


def rol_de(usuario):
    if not usuario.is_authenticated:
        return None
    perfil, _ = Perfil.objects.get_or_create(usuario=usuario)
    return perfil.rol


def es_directivo(usuario):
    return rol_de(usuario) == Perfil.DIRECTIVO


def solo_docente(vista):
    """Bloquea con 403 a quien no sea docente. Va debajo de @login_required."""
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        if es_directivo(request.user):
            raise PermissionDenied
        return vista(request, *args, **kwargs)
    return envoltura