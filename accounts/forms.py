"""Form users."""

from phonenumber_field.formfields import PhoneNumberField

# Django
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Models
from .models import Usuario, Perfil

class UserForm(UserCreationForm):
    """Formulario de registro de usuarios."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Nombres'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Apellidos'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input100','placeholder':'Email'}))
    celular = PhoneNumberField(region='CO', widget=forms.NumberInput(attrs={'class':'input100','placeholder':'Celular'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Confirmar contraseña'}))
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'celular', 'password1', 'password2',)


class ProfileForm(ModelForm):
    """Formulario para compllementar información empresarial"""
    nom_empresa = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Nombre de la Empresa'}))
    nit = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'NIT', 'type':'number'}))    
    telefono = PhoneNumberField(region='CO', widget=forms.NumberInput(attrs={'class':'input100','placeholder':'Teléfono'}))
    ciudad = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Ciudad(es) de operación'}))
    presupuesto_min = forms.DecimalField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Monto mínimo de contratación', 'type':'number'}))
    presupuesto_max = forms.DecimalField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Monto máximo de contratación', 'type':'number'}))
    activ_economica = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Actividad(es) económica(s)'}))
    
    class Meta:
        model = Perfil
        fields = ['nom_empresa', 'nit', 'telefono', 'ciudad', 'presupuesto_min', 'presupuesto_max', 'activ_economica']

