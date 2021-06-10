from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.signin),
    path('signin', views.signin),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('users/create', views.create_user),
]