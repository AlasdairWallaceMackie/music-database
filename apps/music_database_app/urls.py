from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('bands', views.band_list),
    path('bands/<int:id>', views.show_band),
    path('bands/new', views.new_band),
    path('bands/create', views.create_band),
    path('albums', views.album_list),
    path('albums/<int:id>', views.show_album),
    path('albums/new', views.new_album),
    path('albums/create', views.create_album),
    path('users', views.user_list),
    path('users/<int:id>', views.show_user),
    #Delete band
    #Delete album
]