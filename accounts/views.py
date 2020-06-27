from django.shortcuts import render, redirect
from .models import Usuario, Perfil
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def creaUsuarioView(request):
    # Registro de usuarios view

    if request.method == 'POST':
        email = request.POST['email']
        passwd = request.POST['password1']
        passwd_confirmation = request.POST['password2']

        if passwd != passwd_confirmation:
            return render(request, 'account/signup.html', {'error': 'Las contraseñas no coinciden'})

        try:
            user = Usuario.objects.create_user(
                username=email,
                email=email,
                password=passwd
            )

        except IntegrityError:
            return render(request, 'account/signup.html', {'error': 'Ya existe un usuario registrado con este correo'})

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.tipo_documento = request.POST['tipo_documento']
        user.num_documento = request.POST['num_documento']
        user.celular = request.POST['celular']
        user.save()

        profile = Perfil(usuario=user)
        profile.save()
        new_user = authenticate(email=email,
                                password=passwd,
                                )
        login(request, new_user)

        return redirect('welcome_page')

    return render(request, 'account/signup.html')


@login_required
def logoutView(request):
    # Logout
    logout(request)
    return redirect('home_page')
