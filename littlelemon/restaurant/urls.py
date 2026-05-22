from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # ── SPLASH (root) ────────────────────────────────────────────
    path('', views.splash, name='splash'),

    # ── EXISTING PAGES ───────────────────────────────────────────
    path('home/',    views.home,    name='home'),
    path('about/',   views.about,   name='about'),
    path('menu/',    views.menu,    name='menu'),
    path('menu/<int:pk>/',  views.menu_detail, name='menu_detail'),
    path('location/', views.location, name='location'),

    # ── BOOKING ──────────────────────────────────────────────────
    path('book/',                        views.book,            name='book'),
    path('booking/<int:pk>/success/',    views.booking_success, name='booking_success'),
    path('bookings/',                    views.bookings_list,   name='bookings_list'),
    path('my-bookings/',                 views.my_bookings,     name='my_bookings'),
    path('my-bookings/<int:pk>/edit/',   views.booking_edit,    name='booking_edit'),
    path('my-bookings/<int:pk>/cancel/', views.booking_cancel,  name='booking_cancel'),

    # ── REVIEWS ──────────────────────────────────────────────────
    path('menu/<int:pk>/review/',        views.add_review,    name='add_review'),
    path('review/<int:pk>/delete/',      views.delete_review, name='delete_review'),

    # ── CART ─────────────────────────────────────────────────────
    path('cart/',                        views.cart_view,   name='cart'),
    path('cart/add/<int:pk>/',           views.cart_add,    name='cart_add'),
    path('cart/remove/<int:pk>/',        views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/',        views.cart_update, name='cart_update'),

    # ── CHECKOUT & ORDERS ─────────────────────────────────────────
    path('checkout/',                    views.checkout,      name='checkout'),
    path('checkout/coupon/',             views.apply_coupon,  name='apply_coupon'),
    path('orders/',                      views.order_list,    name='order_list'),
    path('orders/<int:pk>/',             views.order_detail,  name='order_detail'),
    path('orders/<int:pk>/status.json/', views.order_status_json, name='order_status_json'),

    # ── LOYALTY ──────────────────────────────────────────────────
    path('loyalty/',                     views.loyalty_dashboard, name='loyalty'),

    # ── ADMIN DASHBOARD ───────────────────────────────────────────
    path('admin-bookings/',              views.admin_bookings,               name='admin_bookings'),
    path('admin-bookings/<int:pk>/status/', views.admin_booking_update_status, name='admin_booking_update_status'),

    # ── ADMIN ORDER DASHBOARD ────────────────────────────────────────────────────
    path('admin-orders/',                 views.admin_orders,                name='admin_orders'),
    path('admin-orders/<int:pk>/status/', views.admin_order_update_status,   name='admin_order_update_status'),

    # ── AUTH ─────────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'),           name='logout'),

    # ── API ──────────────────────────────────────────────────────
    path('api/', include('restaurant.api.urls')),
]
