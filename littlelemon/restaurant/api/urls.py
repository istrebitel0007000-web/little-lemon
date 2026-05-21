from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from .views import (
    MenuViewSet, BookingViewSet, RegisterView,
    OrderViewSet, ReviewViewSet,
)

router = DefaultRouter()
router.register(r'menu',     MenuViewSet,   basename='menu')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'orders',   OrderViewSet,  basename='order')
router.register(r'reviews',  ReviewViewSet, basename='review')

urlpatterns = [
    path('',          include(router.urls)),
    path('register/', RegisterView.as_view(),          name='api-register'),
    path('token/',    TokenObtainPairView.as_view(),   name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/',  TokenVerifyView.as_view(),  name='token_verify'),
    path('auth/',     include('rest_framework.urls')),
]
