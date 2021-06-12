from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import *


def home(request):
    return HttpResponse("<h1>Home Page</h1>")

def band_list(request):
    return HttpResponse("<h2>Band List</h2>")

def show_band(request, id):
    return HttpResponse(f"Band ID: {id}")

def new_band(request):
    return HttpResponse(f"Form to add a new band")

def create_band(request):
    return HttpResponse("Placeholder to add band to database")


def album_list(request):
    return HttpResponse("List of albums")

def show_album(request, id):
    return HttpResponse("Album ID: {id}")

def new_album(request):
    return HttpResponse("Form to add new album")

def create_album(request):
    return HttpResponse("Placeholder to add album to database")

def user_list(request):
    return HttpResponse("List of users")

def show_user(request, id):
    return HttpResponse("User id: {id}")