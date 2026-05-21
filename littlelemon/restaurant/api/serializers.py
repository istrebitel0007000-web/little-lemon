from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from restaurant.models import Booking, Menu, Order, OrderItem, Review, Coupon


# ── EXISTING SERIALIZERS (unchanged) ───────────────────────────────────────────

class MenuSerializer(serializers.ModelSerializer):
    image          = serializers.ImageField(required=False, allow_null=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model  = Menu
        fields = ['id', 'name', 'price', 'image', 'description', 'category',
                  'is_available', 'average_rating']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Booking
        fields = ['id', 'first_name', 'last_name', 'guest_number',
                  'comment', 'date', 'time', 'status']

    def validate_guest_number(self, value):
        if value < 1:
            raise serializers.ValidationError("Guest count must be at least 1.")
        if value > 50:
            raise serializers.ValidationError("Guest count cannot exceed 50.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, required=True,
                                      validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email     = serializers.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user     = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ── NEW SERIALIZERS ─────────────────────────────────────────────────────────────

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    subtotal       = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items    = OrderItemSerializer(many=True, read_only=True)
    total    = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model  = Order
        fields = ['id', 'username', 'status', 'notes', 'items', 'total',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']
