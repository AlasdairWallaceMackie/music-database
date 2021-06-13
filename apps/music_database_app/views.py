from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from django_countries import countries


def home(request):
    return render(request, 'home.html')

def band_list(request):
    return render(request, 'band_list.html')

def show_band(request, id):
    context = {
        'band': Band.objects.get(id = id)
    }
    return render(request, 'show_band.html', context)

def new_band(request):
    context = {
        'countries': countries
    }

    return render(request, 'new_band.html', context)

def create_band(request):
    if request.method == "POST":    
        errors = Band.objects.basic_validator(request.POST)
        if errors:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/new_band')

        new_band = Band.objects.create(
            name = request.POST['name'],
            genre = request.POST['genre'],
            founded = request.POST['founded'],
            country = request.POST['country'],
            status = request.POST['status'],
        )
    
    return redirect(f'/bands/{new_band.id}')



def album_list(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'album_list.html', context)

def show_album(request, id):
    return HttpResponse("Album ID: {id}")

def create_album(request):
    return HttpResponse("Placeholder to add album to database")

def user_list(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'user_list.html', context)

def show_user(request, id):
    return HttpResponse("User id: {id}")









def create_user(request):
    if request.method == "POST":
        # errors = User.objects.basic_validator(request.POST)

        # if errors:
        #     for k,v in errors.items():
        #         messages.error(request, v)
        #     return redirect('/register')

        new_user = User.objects.create(
            username = request.POST['username'].lower(),
            email = request.POST['email'],
            password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() ).decode()
        )

        request.session['current_user_id'] = new_user.id

    return redirect(f'/users/{new_user.id}')

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