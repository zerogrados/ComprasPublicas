from django.urls import include, path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registro/', views.creaUsuarioView, name='registro'),
    path('cerrar_sesion/', views.logoutView, name='cerrar_sesion'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
        # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset_form.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]