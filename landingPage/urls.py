from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    # Index
    path('', views.landingView, name='home_page'),
    path('contact_me/', views.contactView, name='contact_page')
]