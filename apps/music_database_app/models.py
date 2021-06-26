from os import error
from django.db import models
from datetime import date, datetime

from django_countries.fields import CountryField
from django_countries import countries
from ..login_and_reg_app.models import *
import re

class Band_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        try:
            errors = errors | self.name_validator(post_data['name'])
        except:
            errors['no_name'] = "Please enter a name for this band"
        print(f"DATA: {errors}")
        try:
            errors = errors | self.genre_validator(post_data['genre'])
        except:
            errors['no_genre'] = "Please enter a valid genre"
        print(f"DATA: {errors}")
        try:
            errors = errors | self.founded_validator(post_data['founded'])
        except:
            errors['no_year'] = "Please enter a year"
        print(f"DATA: {errors}")
        try:
            errors = errors | self.country_validator(post_data['country'])
        except:
            errors['no_country'] = "Please enter a country"
        print(f"DATA: {errors}")
        try:
            errors = errors | self.status_validator(post_data['status'])
        except:
            errors['no_status'] = "Please enter a status"

        print(f"FINAL DATA: {errors}")
        
        return errors

    ####################################

    def name_validator(self, post_data):
        errors = {}
        # print("TRIGGER******************************")
        # print(f"DATA: {post_data}")
        if len(post_data) < 1:
            print("NO NAME")
            errors['no_name'] = "Please enter a name for this band"

        if len(post_data) > 128:
            errors['name_too_long'] = "Name is too long"

        if Band.objects.filter( name = post_data.title() ):
            errors['duplicate_band'] = "Band already exists in database"


        # print(f"ERRORS: {errors}")
        return errors

    def genre_validator(self, post_data):
        errors = {}

        GENRE_REGEX = re.compile( r"^[A-Z][a-zA-Z\-\'\s]{2,32}$" )
        if not GENRE_REGEX.match( post_data ):
            errors['invalid_genre'] = "Please enter a valid genre name"

        return errors

    def founded_validator(self, post_data):
        errors = {}

        try:
            if int(post_data) < 1700:
                errors['invalid year'] = "Please enter a valid year"
            if int(post_data) > int( date.today().year ):
                errors['future_year'] = "Year cannot be in the future"
        except:
            errors['invalid year'] = "Please enter a valid year"

        return errors

    def country_validator(self, post_data):
        errors = {}

        if post_data not in countries:
            errors['invalid_country'] = "Please choose a valid country"

        return errors

    def status_validator(self, post_data):
        errors = {}

        if int(post_data) < 0 or int(post_data) > 2:
            errors['invalid_status'] = "Invalid Status"

        return errors


class Album_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        try:
            errors = errors | self.validate_title(post_data['title'])
        except:
            errors['no_title'] = "Please add a title"

        if 'band' not in post_data:
            errors['no_band'] = "No band associated with album"

        if not Band.objects.filter(id = post_data['band']):
            errors['band_not_found'] = "Associated band not found"

        try:
            errors = errors | self.validate_release_date(post_data['release_date'])
        except:
            errors['no_release_date'] = "Please enter a release date"

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
    
    def validate_title(self, post_data):
        errors = {}

        if len(post_data) < 1:
            errors['no_title'] = "Please add a title"

        if len(post_data) > 128:
            errors['title_too_long'] = "Title is too long"

        return errors

    def validate_release_date(self, post_data):
        errors = {}
        try:
            if datetime.strptime(post_data, '%Y-%m-%d').date() > date.today():
                errors['release_date_in_future'] = "Release date cannot be in the future"
        except:
            errors['no_release_date'] = "Please enter a release date"

        return errors


class Rating_Manager(models.Manager):
    def basic_validator(self, post_data):
        MAX_RATING = 5
        errors = {}

        if int(post_data['rating']) < 0 or int(post_data['rating']) > MAX_RATING:
            errors["invalid_rating_value"] = f"Rating can only be between 1 and {MAX_RATING}"

        #! CHECK TO MAKE SURE SINGLE USER DOESN'T RATE MORE THAN ONCE

        return errors

#########################
#########################

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
            0: "Split-Up",
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
    
    ##Foreign Keys:
    # ratings 
    objects = Album_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"< Album ID: {self.id} | {self.title} by {self.band.name}>"

    def rating_avg(self):
        sum = 0
        for rating in self.ratings.all():
            sum += rating.value
        # avg = float( sum / )
        return round( float( sum / self.ratings.count() ), 2)

    def get_user_rating(self, user):
        for rating in self.ratings.all():
            if rating.user == user:
                return rating.value
        return 0

class Rating(models.Model):
    value = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")

    objects = Rating_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def song_list(self):
    #     list = []
    #     for song in self.songs:
    #         list.append(song)
        
    #     sorted = False
    #     while(sorted == False and len(list) > 1):
    #         for i in range( len(list)-1 ):
    #             sorted = True
    #             if list[i].track_number > list[i+1].track_number:
    #                 list[i], list[i+1] = list[i+1], list[i]
    #                 sorted = False

    #     return list

# class Song(models.Model):
#     title = models.CharField(max_length=128)
#     length = models.IntegerField() #In Seconds
#     album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
#     track_number = models.IntegerField()
#     band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="songs")

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def length_in_min_sec(self):
#         return f"{ int(self.length / 60) }:{ self.length % 60 }"