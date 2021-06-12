from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import *
import bcrypt
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def band_list(request):
    return render(request, 'band_list.html')

def show_band(request, id):
    return render(request, 'show_band.html')

def new_band(request):
    return render(request, 'new_band.html')

def create_band(request):
    return HttpResponse("Placeholder to add band to database")



def album_list(request):
    return render(request, 'album_list.html')

def show_album(request, id):
    return HttpResponse("Album ID: {id}")

def create_album(request):
    return HttpResponse("Placeholder to add album to database")

def user_list(request):
    return HttpResponse("List of users")

def show_user(request, id):
    return HttpResponse("User id: {id}")

def create_user(request):
    return HttpResponse("Placeholder for create_user logic")



def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    #Check credentials
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')