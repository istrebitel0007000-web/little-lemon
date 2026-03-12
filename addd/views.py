from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import ReservationForm
from .models import Reservation

# Create your views here.
def function_view(request):
    return HttpResponse("Hello from function!")


def hello_world(request):
    return HttpResponse('Hello, World!')   


class HelloMalaysia(View):
    def get(self, request):
        return HttpResponse("Hello Malaysia")


def home(request):
    return HttpResponse("Welcome to Home Page!")


def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation_list.html', {'reservations': reservations})
    