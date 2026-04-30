from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('booking/<int:pk>/success/', views.booking_success, name='booking_success'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('location/', views.location, name='location'),
    path('bookings/', views.bookings_list, name='bookings_list'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('api/', include('restaurant.api.urls')),
]
