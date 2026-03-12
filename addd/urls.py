from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
    path('class/', include('hello_world.urls')),
    path("function/", views.function_view), 
    path('reservation/', views.reservation_list, name='reservation_list'),
]
