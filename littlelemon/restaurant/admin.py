from django.contrib import admin
from .models import Booking, Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'guest_number', 'comment']
    search_fields = ['first_name', 'last_name']