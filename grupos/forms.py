from django import forms 
from .models import Grupo, Estudiante

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'grado', 'anio']
        widgets = {'anio': forms.NumberInput(attrs={'min': 2020, 'max': 2100})}

    def __init__(self, *args, docente=None, **kwargs):
        self.docente = docente
        super().__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        return nombre

    def clean_anio(self):
        anio = self.cleaned_data['anio']
        if not 2020 <= anio <= 2100:
            raise forms.ValidationError('El año debe estar entre 2020 y 2100.')
        return anio

    def clean(self):
        datos = super().clean()
        nombre, anio = datos.get('nombre'), datos.get('anio')
        if self.docente and nombre and anio:
            repetido = Grupo.objects.filter(docente=self.docente, nombre__iexact=nombre, anio=anio)
            if self.instance.pk:
                repetido = repetido.exclude(pk=self.instance.pk)
            if repetido.exists():
                raise forms.ValidationError('Ya tienes un grupo con ese nombre en ese año.')
        return datos

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'codigo']

    def __init__(self, *args, grupo=None, **kwargs):
        self.grupo = grupo
        super().__init__(*args, **kwargs)

    def clean_nombres(self):
        valor = self.cleaned_data['nombres'].strip()
        if len(valor) < 2:
            raise forms.ValidationError('Los nombres deben tener al menos 2 caracteres.')
        return valor

    def clean_apellidos(self):
        valor = self.cleaned_data['apellidos'].strip()
        if len(valor) < 2:
            raise forms.ValidationError('Los apellidos deben tener al menos 2 caracteres.')
        return valor

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip()
        if self.grupo:
            repetido = Estudiante.objects.filter(grupo=self.grupo, codigo__iexact=codigo)
            if self.instance.pk:
                repetido = repetido.exclude(pk=self.instance.pk)       
            if repetido.exists():
                raise forms.ValidationError('Ya hay un estudiante con ese cÃ³digo en este grupo.')
        return codigo