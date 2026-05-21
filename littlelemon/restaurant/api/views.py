from rest_framework import viewsets, generics, permissions, filters
from rest_framework.permissions import AllowAny

from restaurant.models import Booking, Menu, Order, Review
from .serializers import (
    MenuSerializer, BookingSerializer, RegisterSerializer,
    OrderSerializer, ReviewSerializer,
)


# ── EXISTING VIEWSETS (unchanged) ──────────────────────────────────────────────

class MenuViewSet(viewsets.ModelViewSet):
    queryset           = Menu.objects.all().order_by('name')
    serializer_class   = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'category']
    ordering_fields    = ['name', 'price']


class BookingViewSet(viewsets.ModelViewSet):
    queryset           = Booking.objects.all().order_by('-id')
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['first_name', 'last_name']


class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [AllowAny]


# ── NEW VIEWSETS ────────────────────────────────────────────────────────────────

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Users can only see their own orders via API."""
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__menu_item').order_by('-created_at')


class ReviewViewSet(viewsets.ModelViewSet):
    """Anyone can read reviews; only authenticated users can post."""
    serializer_class   = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['menu_item__name']

    def get_queryset(self):
        return Review.objects.select_related('user', 'menu_item').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
