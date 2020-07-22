# Django
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import views as auth_views

# Models
from .models import Usuario, Perfil

# Utilities
import json

# Forms
from .forms import UserForm, ProfileForm

def loginView(request):
    if request.method == 'POST':
        try:
            user = authenticate(email=request.POST['login'],
                            password=request.POST['password'],
            )
            login(request, user)
            return redirect('welcome_page')
        except:
            return render(request, 'account/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'account/login.html')


def createUserView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = Usuario.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )

            except IntegrityError:
                return render(request, 'account/signup.html', {'error': 'Ya existe un usuario registrado con este correo', 'form': form})

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.celular = form.cleaned_data['celular']
            user.save()
            profile = Perfil(usuario=user)
            profile.save()
            #import pdb; pdb.set_trace()
            new_user = authenticate(email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('welcome_page')

        else:

            try:
                if form.errors['celular']:
                    form.errors['celular'] = 'Ingrese un teléfono valido (Ej: 3001112233)'
            except:
                pass
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})


#@login_required
def updateProfileView(request):
    if request.method == 'GET':
        form = ProfileForm()
        return render(request, 'account/profile_info.html', {'form': form})

    elif request.method == 'POST':
        form = ProfileForm(request.POST)
        return render(request, 'account/profile_info.html', {'form': form})
    
@login_required
def logoutView(request):
    # Logout
    logout(request)
    return redirect('home_page')


class ResetPasswordView(auth_views.PasswordResetView):
    def form_valid(self, form):
        usuario = None
        email = form.cleaned_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
        except:
            pass
        if usuario:
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            return super().form_valid(form)

        else:
            form.errors['email'] = 'No existe un usuario con el correo ingresado'
            return render(self.request, 'account/password_reset_form.html', {'form': form})

def cod(request):
    #with open('colombia.json') as json_file:
    #    data = json.load(json_file)
    #    print(data)
    return render(request, 'account/set_code_unspsc.html')