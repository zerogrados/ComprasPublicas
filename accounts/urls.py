from django.urls import include, path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup_form/', views.createUserView, name='registro'),
    path('login/', views.loginView, name='login'),
    path('logout_/', views.logoutView, name='cerrar_sesion'),
    path(
        'change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
        # Forget Password
    path('password_reset/',
         views.ResetPasswordView.as_view(
             template_name='account/password_reset_form.html',
             subject_template_name='account/password_reset_subject.txt',
             html_email_template_name='account/password_reset_email.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('cod/', views.cod, name="cod"),
    
    # PROFILE
    path('profile_form/', views.updateProfileView, name='perfil_empresarial'),
]