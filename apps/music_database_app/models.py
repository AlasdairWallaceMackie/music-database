from django.db import models
from django.db.models.fields import DateField

class Band(models.Model):
    name = models.CharField(max_length=128)
    genre = models.CharField(max_lenth=16)
    founded = models.IntegerField()
    country = models.CharField(max_length=32)
    status = models.IntegerField()
        # 2 = Active, 1 = Hiatus, 0 = Inactive

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Album(models.Model):
    title = models.CharField(max_length=128)
    #songs

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)