from django.db import models
from django.db.models import Count
from datetime import date, datetime
import re

class User_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        EMAIL_REGEX = re.compile( r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9+_-]+\.[A-Za-z0-9.]+$' )
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Please enter a valid email address"
        
        if len(post_data['email']) > 64:
            errors['email_length'] = "Email is too long"


        if User.objects.filter( email = post_data['email'].lower() ):
            print("Duplicate email found")
            errors['duplicate_email'] = f"Email '{post_data['email']}' is already in use"
        
        if len(post_data['username']) < 3 or len(post_data['username']) > 32:
            errors['username_length'] = "Username must be between 3 and 32 characters"

        if User.objects.filter( username = post_data['username'].lower() ):
            errors['duplicate_username'] = f"Username '{post_data['username']}' already exists"

        if len(post_data['password']) < 8:
            errors['short_password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['confirm']:
            errors['no_match'] = "Passwords didn't match"

        return errors

class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    password = models.TextField()
    ##Foreign Keys
    # Band.added_by
    # Album.added_by
    # Band.last_edited_by
    # Album.last_edited_by
    # ratings
        
    objects = User_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_contributions(self):
        return Count(self.added_bands) + Count(self.added_albums)

    def number_of_bands_added(self):
        return Count(self.added_bands)

    def number_of_albums_added(self):
        return Count(self.added_albums)