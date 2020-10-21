# Django
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

# Models
from .models import Usuario, Perfil, Ciudad, CodUNSPSC

# Utilities
import json
from .utilities.update_profiles import updateProfile

# Forms
from .forms import UserForm, ProfileForm


def loginView(request):
    if request.method == 'POST':
        try:
            user = authenticate(email=request.POST['login'],
                                password=request.POST['password'],
                                )
            login(request, user)
            return redirect('user_oportunities')
        except:
            return render(request, 'account/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'account/login.html')


def createUserView(request):
    try:
        request.session['subscription'] = request.GET['subscription']
    except:
        pass
    if request.user.is_authenticated:
        return redirect('subscription_validate')

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
            
            new_user = authenticate(email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('enterprise_profile')

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


@login_required
def updateProfileView(request):
    if request.method == 'GET':
        profile = request.user.perfil
        ciudades = list(Ciudad.objects.filter(perfil__id=profile.id).values_list('codigo_ciudad', flat=True))
        activ_economica = list(CodUNSPSC.objects.filter(perfil__id=profile.id).values_list('perfil', flat=True))
        activ_economica = list(map(lambda activ_economica: activ_economica.codigo, profile.activ_economica.all()))
        form = ProfileForm(initial={'nom_empresa': profile.nom_empresa,
                                    'nit': profile.nit, 'telefono': profile.telefono,
                                    'ciudad': profile.ciudades, 
                                    'presupuesto_min': profile.presupuesto_min,
                                    'presupuesto_max': profile.presupuesto_max,
                                    'activ_economica': profile.activ_economica
                                    })
        if profile.nom_empresa == None:
            return render(request, 'account/profile_info.html', {'form': form, 'profile': profile,
                                                             'ciudades': ciudades, 'activ_economica': activ_economica})
        else:
            return render(request, 'account/profile_info_update.html', {'form': form, 'profile': profile,
                                                             'ciudades': ciudades, 'activ_economica': activ_economica})

    elif request.method == 'POST':
        updateProfile(request)
        return redirect('subscription_validate')
        


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
