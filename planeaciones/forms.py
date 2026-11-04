from django import forms

from .models import Planeacion


class PlaneacionForm(forms.ModelForm):
    """Formulario para crear y editar planeaciones, con reglas del servidor."""

    class Meta:
        model = Planeacion
        fields = ['asignatura', 'grado', 'semana', 'objetivos',
                  'temas', 'actividades', 'recursos']
        widgets = {
            'semana': forms.NumberInput(attrs={'min': 1, 'max': 52}),
            'objetivos': forms.Textarea(attrs={'rows': 3}),
            'temas': forms.Textarea(attrs={'rows': 3}),
            'actividades': forms.Textarea(attrs={'rows': 4}),
            'recursos': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, docente=None, **kwargs):
        # La vista nos pasa el docente para validar sus propias planeaciones
        self.docente = docente
        super().__init__(*args, **kwargs)

    def clean_objetivos(self):
        # Regla: los objetivos deben tener un mínimo de contenido
        objetivos = self.cleaned_data['objetivos'].strip()
        if len(objetivos) < 10:
            raise forms.ValidationError(
                'Los objetivos deben tener al menos 10 caracteres.'
            )
        return objetivos

    def clean(self):
        datos = super().clean()
        asignatura = datos.get('asignatura')
        grado = datos.get('grado')
        semana = datos.get('semana')
        # Regla: un docente no repite asignatura, grado y semana
        if self.docente and asignatura and grado and semana:
            repetida = Planeacion.objects.filter(
                docente=self.docente, asignatura=asignatura,
                grado__iexact=grado, semana=semana,
            )
            if self.instance.pk:
                # Al editar, no se compara la planeación consigo misma
                repetida = repetida.exclude(pk=self.instance.pk)
            if repetida.exists():
                raise forms.ValidationError(
                    'Ya tienes una planeación de esa asignatura, grado y semana.'
                )
        return datos