from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, Menu

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookings_list')  # after booking, go to list page
    return render(request, 'book.html', {'form': form})

def bookings_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings_list.html', {'bookings': bookings})

def menu(request):
    menu = Menu.objects.all()
    return render(request, 'menu.html', {'menu': menu})