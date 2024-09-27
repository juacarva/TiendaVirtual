from django import forms
from .models import DireccionEnvio, Invitado
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')