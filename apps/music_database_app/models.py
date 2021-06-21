from os import error
from django.db import models
from datetime import date, datetime

from django_countries.fields import CountryField
from ..login_and_reg_app.models import *
import re

class Band_Manager(models.Manager):
    def basic_validator(self, post_data, type="create"):
        errors = {}

        if (type == "update" and post_data['name'] != "") or type=="create":
            if len( post_data['name'] ) < 1 or len( post_data['name'] )> 128:
                errors['name_length'] = "Invalid band name length"

            if Band.objects.filter( name = post_data['name'].title() ):
                errors['duplicate_band'] = "Band already exists in database"


        if (type == "update" and 'genre' in post_data ) or type=="create":
            if 'genre' not in post_data:
                errors['no_genre'] = "Please choose a genre"
            else:
                GENRE_REGEX = re.compile( r"^[a-zA-Z\-\'\s]{2,32}$" )
                if not GENRE_REGEX.match( post_data['genre'] ):
                    errors['invalid_genre'] = "Please enter a valid genre name"

        if (type == "update" and post_data['founded'] != "") or type=="create":
            try:
                if int(post_data['founded']) < 1700 or int(post_data['founded']) > int( date.today().year ):
                    errors['invalid year'] = "Please enter a valid year"
            except:
                errors['no_year'] = "Please enter a year"

        if (type == "update" and 'country' in post_data) or type=="create":
            if 'country' not in post_data:
                errors['no_country'] = "Please enter a country"

        if (type == "update" and post_data['country'] != "") or type=="create":
            try:
                if int(post_data['status']) < 0 or int(post_data['status']) > 2:
                    errors['invalid_status'] = "Invalid Status"
            except:
                errors['no_status'] = "Please enter a status"
        
        return errors


class Album_Manager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['title']) < 1:
            errors['no_title'] = "Please add a title"

        if len(post_data['title']) > 128:
            errors['title_too_long'] = "Title is too long"

        if 'band' not in post_data:
            errors['no_band'] = "No band associated with album"

        if not Band.objects.filter(id = post_data['band']):
            errors['band_not_found'] = "Associated band not found"

        if not post_data['release_date']:
            errors['no_release_date'] = "Please enter a full release date (Month, day, year)"
        elif datetime.strptime(post_data['release_date'], '%Y-%m-%d').date() > date.today():
            errors['release_date_in_future'] = "Release date cannot be in the future"

        if not post_data['added_by_id']:
            errors['no_uploader'] = "No uploader associated"

        if not User.objects.filter(id = post_data['added_by_id']):
            errors['invalid_uploader'] = "Invalid uploader"

        return errors
    
    def files_validator(self, post_data):
        errors = {}
        
        if 'cover_art' not in post_data:
            errors['no_cover_art'] = "Please upload cover art for this album"

        return errors
    
    # def validate_title()
    # def validate_band()
    # def validate_release_date()
    # def validate_added_by_id()


class Band(models.Model):
    name = models.CharField(max_length=128)
    genre = models.CharField(max_length=32)
    founded = models.IntegerField() #Year
    country = CountryField()
    status = models.IntegerField()
        # 2 = Active, 1 = Hiatus, 0 = Inactive
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_bands")
    last_edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_bands")

    #FK: albums
    #FK: songs
    objects = Band_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Band ID: {self.id} -- {self.name}>"

    def uploader_id(self):
        return self.added_by.id

    def albums_recent_first(self):
        return self.albums.all().order_by('-release_date')

    def get_status(self):
        statuses = {
            0: "Inactive",
            1: "Hiatus",
            2: "Active"
        }
        return f"{statuses[self.status]}"




class Album(models.Model):
    title = models.CharField(max_length=128)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField()
    cover_art = models.ImageField(blank = True, null = True, upload_to='cover_art/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_albums")
    last_edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_albums")
    
    #FK: songs
    objects = Album_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< Album ID: {self.id} | {self.title} by {self.band.name}>"

    def song_list(self):
        list = []
        for song in self.songs:
            list.append(song)
        
        sorted = False
        while(sorted == False and len(list) > 1):
            for i in range( len(list)-1 ):
                sorted = True
                if list[i].track_number > list[i+1].track_number:
                    list[i], list[i+1] = list[i+1], list[i]
                    sorted = False

        return list

    def genre(self):
        return self.band.genre

class Song(models.Model):
    title = models.CharField(max_length=128)
    length = models.IntegerField() #In Seconds
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    track_number = models.IntegerField()
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="songs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def format_length(self):
        return f"{ int(self.length / 60) }:{ self.length % 60 }"