from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ── EXISTING MODELS (unchanged) ────────────────────────────────────────────────

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    comment = models.CharField(max_length=1000)
    # NEW fields added to existing Booking
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    status = models.CharField(max_length=20, choices=[
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Menu(models.Model):
    name  = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    # NEW fields added to existing Menu
    description   = models.TextField(blank=True)
    category      = models.CharField(max_length=100, blank=True)
    is_available  = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


# ── NEW MODELS ──────────────────────────────────────────────────────────────────

class Review(models.Model):
    """Star rating + comment on a menu item."""
    menu_item  = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    rating     = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('menu_item', 'user')   # one review per user per item

    def __str__(self):
        return f'{self.user.username} — {self.menu_item.name} ({self.rating}★)'


class Order(models.Model):
    """An order placed by a logged-in user."""
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('preparing',  'Preparing'),
        ('ready',      'Ready'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes      = models.TextField(blank=True)

    def __str__(self):
        return f'Order #{self.pk} by {self.user.username} [{self.status}]'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    """One line in an Order."""
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu,  on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}× {self.menu_item.name}'

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity


class Cart(models.Model):
    """Persistent cart — one per user."""
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())

    @property
    def item_count(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    """One line in a Cart."""
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'menu_item')

    def __str__(self):
        return f'{self.quantity}× {self.menu_item.name}'

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity


class LoyaltyAccount(models.Model):
    """Points wallet — one per user."""
    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty')
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} — {self.points} pts'

    def add_points(self, amount):
        """1 point per 1 MYR spent (rounded down)."""
        self.points += int(amount)
        self.save()

    def redeem_points(self, points_to_redeem):
        """Returns discount amount. 100 pts = 1 MYR off."""
        if points_to_redeem > self.points:
            raise ValueError('Not enough points')
        self.points -= points_to_redeem
        self.save()
        return round(points_to_redeem / 100, 2)


class Coupon(models.Model):
    """Discount coupon codes."""
    DISCOUNT_TYPES = [
        ('percent', 'Percentage'),
        ('fixed',   'Fixed Amount'),
    ]
    code          = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    value         = models.DecimalField(max_digits=6, decimal_places=2)
    valid_from    = models.DateTimeField(default=timezone.now)
    valid_until   = models.DateTimeField()
    max_uses      = models.PositiveIntegerField(default=100)
    times_used    = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            self.times_used < self.max_uses
        )

    def apply(self, total):
        """Returns discounted total."""
        if self.discount_type == 'percent':
            return round(total * (1 - self.value / 100), 2)
        return max(round(total - self.value, 2), 0)
