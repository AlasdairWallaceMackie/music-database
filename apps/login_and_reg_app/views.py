from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
import bcrypt

def signin(request):
    #Can sign in with either username or email
    return HttpResponse("Sign In Page")

def register(request):
    return HttpResponse("Registration Page")

def login(request):
    #Check credentials
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def create_user(request):
    #Validate and create
    return redirect('/')