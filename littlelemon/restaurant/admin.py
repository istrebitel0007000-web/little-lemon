from django.contrib import admin
from .models import Booking, Menu, Review, Order, OrderItem, Cart, CartItem, LoyaltyAccount, Coupon


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display  = ['name', 'price', 'category', 'is_available']
    list_filter   = ['category', 'is_available']
    search_fields = ['name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'guest_number', 'date', 'time', 'status', 'user']
    list_filter   = ['status', 'date']
    search_fields = ['first_name', 'last_name']
    list_editable = ['status']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['user', 'menu_item', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['user__username', 'menu_item__name']


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'status', 'total', 'created_at']
    list_filter   = ['status']
    search_fields = ['user__username']
    list_editable = ['status']
    inlines       = [OrderItemInline]


@admin.register(LoyaltyAccount)
class LoyaltyAdmin(admin.ModelAdmin):
    list_display  = ['user', 'points']
    search_fields = ['user__username']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display  = ['code', 'discount_type', 'value', 'valid_until', 'times_used', 'is_active']
    list_filter   = ['discount_type', 'is_active']
    search_fields = ['code']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total']
