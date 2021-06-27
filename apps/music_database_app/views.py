from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from django_countries import countries


def home(request):
    context = {
        'recent_bands': Band.objects.all().order_by('-created_at')[:6],
        'newest_albums': Album.objects.all().order_by('-release_date')[:4],
    }
    return render(request, 'home.html', context)

def band_list(request):
    context = {
        'bands': Band.objects.order_by("name")
    }
    return render(request, 'band_list.html', context)

def show_band(request, id):
    context = {
        'band': Band.objects.get(id = id),
        'countries': countries
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
        print(request.POST)
        errors = Band.objects.basic_validator(request.POST)
        if errors:
            print("Errors found when trying to create band")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect('/bands/new')

        current_user = User.objects.get(id = request.session['current_user_id'])

        print("No errors found, adding band to database")
        new_band = Band.objects.create(
            name = request.POST['name'].title(),
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
                messages.error("You are not the original uploader of this band and are not authorized to delete it")
        except:
            print("Deletion failed: Band not found")

    return redirect('/bands')

def update_band(request, id):
    if request.method=="POST":
        if 'current_user_id' not in request.session:
            messages.warning(request, "You need to be logged in to make edits")
            return redirect("/signin")
        else:
            print(f"Request to update band id: {id}")

            try:
                band_to_update = Band.objects.get(id = id)
            except:
                messages.error(request, "Band not found")
                return redirect('/bands')

            errors = {}
            changed = False

            if request.POST['name'] != band_to_update.name:
                errors = errors | Band.objects.name_validator(request.POST['name'])
                print("Name changed")
                changed = True
            if request.POST['genre'] != band_to_update.genre:
                errors = errors | Band.objects.genre_validator(request.POST['genre'])
                print("Genre changed")
                changed = True
            if int(request.POST['founded']) != band_to_update.founded:
                errors = errors | Band.objects.founded_validator(request.POST['founded'])
                print("Year changed")
                changed = True
            if request.POST['country'] != band_to_update.country:
                errors = errors | Band.objects.country_validator(request.POST['country'])
                print("Country changed")
                changed = True
            if int(request.POST['status']) != band_to_update.status:
                errors = errors | Band.objects.status_validator(request.POST['status'])
                print("Status changed")
                changed = True
        
            if errors:
                for k,v in errors.items():
                    messages.error(request, v)
            elif changed==True:
                band_to_update.name = request.POST['name']
                band_to_update.genre = request.POST['genre']
                band_to_update.founded = request.POST['founded']
                band_to_update.country = request.POST['country']
                band_to_update.status = request.POST['status']
                band_to_update.last_edited_by = User.objects.get(id = request.session['current_user_id'])
                band_to_update.save()

                messages.success(request, "Band successfully updated!")
            else:
                messages.warning(request, "No changes were made")

    return redirect(f"/bands/{id}")

def album_list(request):
    context = {
        'albums': Album.objects.order_by("title")
    }
    return render(request, 'album_list.html', context)

def show_album(request, id):
    try:
        album = Album.objects.get(id = id)
    except:
        messages.error(request, "Album not found")
        return redirect('/albums')

    context = {
        'album': album,
        'avg_rating': album.rating_avg(),
        'user_rating': 0,
    }

    if 'current_user_id' in request.session:
        current_user = User.objects.get(id = request.session['current_user_id'])
        context['user_rating'] = album.get_user_rating(current_user)
    
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
        errors | Album.objects.files_validator(request.FILES)
        if errors:
            print("Errors found in form")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f'/bands/{band.id}')

        img = request.FILES['cover_art']
        
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

        errors = {}
        if request.POST['title'] != '':
            errors = errors | Album.objects.validate_title(request.POST['title'])
        if request.POST['release_date'] != '':
            errors = errors | Album.objects.validate_release_date(request.POST['release_date'])        

        if errors:
            print("Errors found when updating album")
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f'/albums/{id}')
        
        # print(f"Title: {request.POST['title']}")
        # print(f"Date: {request.POST['release_date']}")
        # print(f"Artwork: {request.FILES}")
        
        changed = False

        if request.POST['title'] != "":
            print("Updating album title")
            album_to_update.title = request.POST['title']
            changed = True

        if request.POST['release_date'] != "":
            print("Updating album release date")
            album_to_update.release_date = request.POST['release_date']
            changed = True

        if 'cover_art' in request.FILES:
            print("Updating album cover art")
            album_to_update.cover_art = request.FILES['cover_art']
            changed = True


        if changed == True:
            album_to_update.last_edited_by = User.objects.get(id = request.session['current_user_id'])
            album_to_update.save()
            messages.success(request, "Album info updated!")
        else:
            messages.warning(request, "No changes were made")

    return redirect(f'/albums/{id}')


def delete_album(request, id):
    if request.method=="POST":
        print("Deleting album...")
        try:
            album_to_delete = Album.objects.get(id = id)
        except:
            return HttpResponse(f"<h3>Error: The album you are trying to delete does not exist in the database</h3>")
        
        if album_to_delete.added_by.id != request.session['current_user_id']:
            messages.error(request, "You do not have rights to delete this album")
        else:
            album_title = album_to_delete.title
            band_id = album_to_delete.band.id
            album_to_delete.delete()
            print("Album deletion successfull")
            messages.success(request, f'Successfully deleted "{album_title}"')
    
    return redirect(f'/bands/{band_id}')

def user_list(request):
    context = {
        'newest_users': User.objects.order_by("-created_at")[:10],
        'top_contributors': User.objects.annotate(
            total_contributions = ( Count('added_bands') + Count('added_albums') )
        ).filter(
            total_contributions__gt=0
        ).order_by( '-total_contributions' )[:10],
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


def create_rating(request, id):
    if request.method=="POST":
        print("Applying rating to album...")
        try:
            current_user = User.objects.get(id = request.session['current_user_id'])
        except:
            messages.error(request, "You must be logged in to rate albums")
            return redirect('/signin')
        try:
            current_album = Album.objects.get(id = id)
        except:
            messages.error(request, "Album not found")
            return redirect('/albums')

        errors = Rating.objects.basic_validator(request.POST)
        if errors:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/albums/{id}")
        
        user_rating = Rating.objects.filter(user=current_user, album=current_album).first()
        if user_rating:
            print("User already rated this album, changing rating")
            user_rating.value = request.POST['rating']
            user_rating.save()
        else:
            new_rating = Rating.objects.create(
                value = request.POST['rating'],
                album = current_album,
                user = current_user,
            )
        
        messages.success(request, "Rating applied!")
        return redirect(f"/albums/{id}")







def create_user(request):
    if request.method == "POST":
        print("Creating user...")
        errors = User.objects.basic_validator(request.POST)

        if errors:
            for k,v in errors.items():
                print("Errors found when creating user")
                messages.error(request, v)
            return redirect('/register')

        new_user = User.objects.create(
            username = request.POST['username'].lower(),
            email = request.POST['email'],
            password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt() ).decode()
        )
        print("New user successfully created!")

        print("Logging in as new user...")
        request.session['current_user_id'] = new_user.id
        request.session['current_username'] = new_user.username
        messages.success(request, "Account created!")

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
    messages.warning(request, "Successfully logged out")
    return redirect('/')