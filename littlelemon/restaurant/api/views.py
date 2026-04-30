from rest_framework import viewsets, generics, permissions, filters
from rest_framework.permissions import AllowAny

from restaurant.models import Booking, Menu
from .serializers import MenuSerializer, BookingSerializer, RegisterSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('name')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'price']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-id')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name']


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
