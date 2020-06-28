"""Form users."""

from phonenumber_field.formfields import PhoneNumberField

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Models
from .models import Usuario

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

