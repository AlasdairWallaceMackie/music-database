from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from django_countries import countries


def home(request):
    context = {
        'recent_bands': Band.objects.all().order_by('-created_at')[:3],
        'newest_albums': Album.objects.all().order_by('-release_date')[:3],
    }
    return render(request, 'home.html', context)

def band_list(request):
    context = {
        'bands': Band.objects.all()
    }
    return render(request, 'band_list.html', context)

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
        print("Creating band, checking for errors")
        errors = Band.objects.basic_validator(request.POST)
        if errors:
            print("Errors found")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/bands/new')

        current_user = User.objects.get(id = request.session['current_user_id'])

        print("No errors found, adding band to database")
        new_band = Band.objects.create(
            name = request.POST['name'],
            genre = request.POST['genre'],
            founded = request.POST['founded'],
            country = request.POST['country'],
            status = request.POST['status'],
            added_by = current_user,
            last_edited_by = current_user,
        )
    
    messages.success(request, "Band successfully added!")

    return redirect(f'/bands/{new_band.id}')

def delete_band(request, id):
    if request.method == "POST":
        print(f"Band deletion request received for band id: {id}")
        try:
            band_to_delete = Band.objects.get(id = id)
            print(f"Band found. Uploader: {band_to_delete.uploader_id()} - {band_to_delete.added_by.username}")
            if band_to_delete.uploader_id() == request.session['current_user_id']:
                print("Confirmed user is authorized to delete this band")
                name = band_to_delete.name
                band_to_delete.delete()
                messages.warning(request, f"Band '{name}' deleted")
                print(f"Band <'{name}'> successfully deleted")
            else:
                messages.error("You are not the original uploader of this band and you are not authorized to delete it")
        except:
            print("Deletion failed: Band not found")

    return redirect('/bands')


def album_list(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'album_list.html', context)

def show_album(request, id):
    try:
        context = {
            'album': Album.objects.get(id = id)
        }
    except:
        messages.error(request, "Album not found")
        return redirect('/albums')
    
    return render(request, 'show_album.html', context)

def create_album(request):
    if request.method == "POST":
        print("Creating album")

        try:
            band = Band.objects.get(id = request.POST['band'] )
        except:
            print("Error submitting album: Associated band not found")
            return redirect('/bands')
        try:
            current_user = User.objects.get(id = request.session['current_user_id'])
        except:
            messages.error(request, "You must be logged in to submit to the database")
            print("Album submit failed: User not logged in")
            return redirect('/signin')
        
        errors = Album.objects.basic_validator(request.POST)
        if errors:
            print("Errors found in form")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f'/bands/{band.id}')

        try:
            img = request.FILES['cover_art']
        except:
            messages.error(request, "Please upload cover art for this album")
            return redirect(f'/bands/{band.id}')
        
        print("No errors found. Adding album to database")

        new_album = Album.objects.create(
            title = request.POST['title'],
            band = band,
            release_date = request.POST['release_date'],
            cover_art = img,
            added_by = current_user,
            last_edited_by = current_user,
        )
        messages.success(request, "Album successfully added")

    return redirect(f"/bands/{band.id}")

def update_album(request, id):
    if request.method=="POST":
        print(f"Updating album id: {id}")
        try:
            album_to_update = Album.objects.get(id = id)
        except:
            print("Album not found")
            return HttpResponse("<h1>Error: Album not found</h1>")

        errors = Album.objects.update_validator(request.POST)

        if errors:
            print("Errors found when updating album")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f'/albums/{id}')
        
        print(f"Title: {request.POST['title']}")
        print(f"Date: {request.POST['release_date']}")
        print(f"Artwork: {request.FILES}")
        
        changed = False

        if request.POST['title'] != "":
            print("********************Trigger1")
            album_to_update.title = request.POST['title']
            changed = True

        if request.POST['release_date'] != "":
            print("********************Trigger2")
            album_to_update.release_date = request.POST['release_date']
            changed = True

        if changed == True:
            album_to_update.last_edited_by = User.objects.get(id = request.session['current_user_id'])
            album_to_update.save()
            messages.success(request, "Album info updated!")
        else:
            messages.warning(request, "No changes were made")
        return redirect(f'/albums/{id}')

    return HttpResponse(f"Placeholder to update album id: {id}")

def delete_album(request, id):
    return HttpResponse(f"Placeholder to delete album ID: {id}")

def user_list(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'user_list.html', context)

def show_user(request, id):
    try:
        context = {
            'user': User.objects.get(id = id)
        }
    except:
        messages.error(request, "User not found")
        return redirect('/')
    
    return render(request, 'show_user.html', context)









def create_user(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)

        if errors:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/register')

        new_user = User.objects.create(
            username = request.POST['username'].lower(),
            email = request.POST['email'],
            password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() ).decode()
        )

        request.session['current_user_id'] = new_user.id
        request.session['current_username'] = new_user.username

    return redirect(f'/users/{new_user.id}')

def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    if request.method=="POST":
        print("Attempting login...")
        try:
            new_user = User.objects.get(username = request.POST['username'])
        except:
            print("Username not found, checking for email address...")
            try:
                new_user = User.objects.get(email = request.POST['username'])
            except:
                messages.error(request, "Invalid username/email")
                return redirect('/signin')
        try:
            print("Username/email found. Checking password...")
            if bcrypt.checkpw( request.POST['password'].encode(), new_user.password.encode() ):
                request.session['current_user_id'] = new_user.id
                request.session['current_username'] = new_user.username
                messages.success(request, "Successfully logged in!")
                print(f"Login successful for username: {new_user.username}")
                return redirect('/')
            else:
                messages.error(request, "Incorrect password")
        except:
            pass
        
    print("Login failed")
    return redirect('/signin')


def logout(request):
    print("Logging out...")
    request.session.flush()
    return redirect('/')