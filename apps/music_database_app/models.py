from django.db import models
from datetime import date

from django_countries.fields import CountryField
from ..login_and_reg_app.models import *
import re

class Band_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['name']) < 1 or len( post_data['name'] > 128 ):
            errors['name_length'] = "Invalid band name length"

        GENRE_REGEX = re.compile( r"^[a-zA-Z\-\'\s]{2,32}$" )
        if not GENRE_REGEX.match( post_data['genre'] ):
            errors['invalid_genre'] = "Please enter a valid genre name"

        if post_data['founded'] < 1700 or post_data['founded'] > int( date.today().year ) or not post_data['founded'].is_integer():
            errors['invalid year'] = "Please enter a valid year"

        return errors

class Album_Manager(models.Manager):
    def basic_validator(self):
        errors = {}



        return errors

class Genre(models.Model):
    name = models.CharField(max_length=32)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Band(models.Model):
    name = models.CharField(max_length=128)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="bands")
    founded = models.IntegerField() #Year
    country = CountryField()
    status = models.IntegerField()
        # 2 = Active, 1 = Hiatus, 0 = Inactive
    objects = Band_Manager()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_bands")
    last_edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_bands")

    #FK: albums
    #FK: songs
    objects = Band_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Album(models.Model):
    title = models.CharField(max_length=128)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField()
    cover_art = models.ImageField(blank = True, null = True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_albums")
    last_edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_albums")
    
    #FK: songs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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