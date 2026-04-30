from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .forms import BookingForm, RegistrationForm
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
            booking = form.save()
            _send_booking_confirmation(request, booking)
            messages.success(
                request,
                f"Thanks {booking.first_name}! Your booking for "
                f"{booking.guest_number} guest(s) is confirmed."
            )
            return redirect('booking_success', pk=booking.pk)
    return render(request, 'book.html', {'form': form})


def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def bookings_list(request):
    bookings = Booking.objects.all().order_by('-id')
    return render(request, 'bookings_list.html', {'bookings': bookings})


def menu(request):
    query = request.GET.get('q', '').strip()
    items = Menu.objects.all().order_by('name')
    if query:
        items = items.filter(Q(name__icontains=query))
    return render(request, 'menu.html', {'menu': items, 'query': query})


def menu_detail(request, pk):
    item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_detail.html', {'item': item})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def _send_booking_confirmation(request, booking):
    """Send a console-backend email by default (configurable via EMAIL_BACKEND)."""
    user = request.user if request.user.is_authenticated else None
    recipient = getattr(user, 'email', None)
    if not recipient:
        return
    subject = "Your Little Lemon reservation is confirmed"
    body = (
        f"Hi {booking.first_name},\n\n"
        f"Your booking for {booking.guest_number} guest(s) has been received.\n"
        f"Comment: {booking.comment or '(none)'}\n\n"
        f"We look forward to seeing you!\n"
        f"— Little Lemon"
    )
    try:
        send_mail(
            subject, body, settings.DEFAULT_FROM_EMAIL,
            [recipient], fail_silently=True,
        )
    except Exception:
        pass
