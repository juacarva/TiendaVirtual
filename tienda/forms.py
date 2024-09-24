from django import forms
from .models import DireccionEnvio, Invitado

class SeleccionarDireccionForm(forms.ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = ['direccion', 'ciudad', 'codigo_postal', 'pais']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['direccion'].queryset = DireccionEnvio.objects.filter(usuario=user)
        else:
            self.fields['direccion'].queryset = DireccionEnvio.objects.none()

class InvitadoForm(forms.ModelForm):
    class Meta:
        model = Invitado
        fields = ['nombre', 'email']