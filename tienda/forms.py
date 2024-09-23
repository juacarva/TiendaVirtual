from django import forms
from .models import DireccionEnvio, Invitado

class SeleccionarDireccionForm(forms.ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = ['direccion', 'ciudad', 'codigo_postal', 'pais']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SeleccionarDireccionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['direccion'].queryset = DireccionEnvio.objects.filter(usuario=user)




class SeleccionarDireccionForm(forms.ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = ['direccion', 'ciudad', 'codigo_postal', 'pais']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SeleccionarDireccionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['direccion'].queryset = DireccionEnvio.objects.filter(usuario=user)

class InvitadoForm(forms.ModelForm):
    class Meta:
        model = Invitado
        fields = ['nombre', 'email']