from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('bands', views.band_list),
    path('bands/<int:id>', views.show_band),
    path('bands/new', views.new_band),
    path('bands/create', views.create_band),
    path('bands/<int:id>/destroy', views.delete_band),
    path('bands/<int:id>/update', views.update_band),
    path('albums', views.album_list),
    path('albums/<int:id>', views.show_album),
    path('albums/create', views.create_album),
    path('albums/<int:id>/destroy', views.delete_album),
    path('albums/<int:id>/update', views.update_album),
    path('albums/<int:id>/rate', views.create_rating),
    path('users', views.user_list),
    path('users/<int:id>', views.show_user),
    path('users/create', views.create_user),
    path('signin', views.signin),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]