from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Welcome to Home Page!")

def about(request):
    return HttpResponse("About Us")

def book(request):
    return HttpResponse("Book a reservation")

def menu(request):
    return HttpResponse("Menu")