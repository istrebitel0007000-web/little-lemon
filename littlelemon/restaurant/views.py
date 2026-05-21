from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import (
    BookingForm, BookingEditForm, RegistrationForm,
    ReviewForm, CouponForm, CheckoutForm,
)
from .models import (
    Booking, Menu, Review,
    Order, OrderItem, Cart, CartItem,
    LoyaltyAccount, Coupon,
)


# ── HELPERS ─────────────────────────────────────────────────────────────────────

def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def _get_or_create_loyalty(user):
    acc, _ = LoyaltyAccount.objects.get_or_create(user=user)
    return acc


# ── EXISTING VIEWS (unchanged except book now saves user + date/time) ───────────

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def splash(request):
    return render(request, 'restaurant/splash.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            _send_booking_confirmation(request, booking)
            messages.success(
                request,
                f"Thanks {booking.first_name}! Your booking for "
                f"{booking.guest_number} guest(s) is confirmed."
            )
            return redirect('booking_success', pk=booking.pk)
    return render(request, 'book.html', {'form': form})


def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def bookings_list(request):
    bookings = Booking.objects.all().order_by('-id')
    return render(request, 'bookings_list.html', {'bookings': bookings})


def menu(request):
    query = request.GET.get('q', '').strip()
    items = Menu.objects.filter(is_available=True).order_by('name')
    if query:
        items = items.filter(Q(name__icontains=query) | Q(category__icontains=query))
    return render(request, 'menu.html', {'menu': items, 'query': query})


def menu_detail(request, pk):
    item    = get_object_or_404(Menu, pk=pk)
    reviews = item.reviews.select_related('user').order_by('-created_at')
    # check if logged-in user already reviewed this item
    user_review = None
    review_form = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()
    return render(request, 'menu_detail.html', {
        'item':        item,
        'reviews':     reviews,
        'user_review': user_review,
        'review_form': review_form,
    })


def location(request):
    info = {
        'name':    'Little Lemon',
        'address': 'Pavilion Crystal Fountain, Bukit Bintang, 55100 Kuala Lumpur, Malaysia',
        'phone':   '+60 194633835',
        'email':   'istrebitel0007000@gmail.com',
        'hours': [
            ('Monday – Thursday', '11:00 AM – 10:00 PM'),
            ('Friday – Saturday', '11:00 AM – 11:30 PM'),
            ('Sunday',            '12:00 PM – 9:00 PM'),
        ],
        'map_embed_url': (
            'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d313.7!2d101.71299'
            '!3d3.14806!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2'
            '!1s0x31cc362c774e6c9b%3A0x77dbaaedd55aecc3!2sPavilion%20Crystal%20Fountain'
            '!5e0!3m2!1sen!2s!4v1772687579308!5m2!1sen!2s'
        ),
    }
    return render(request, 'location.html', {'info': info})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create loyalty account on registration
            LoyaltyAccount.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def _send_booking_confirmation(request, booking):
    user      = request.user if request.user.is_authenticated else None
    recipient = getattr(user, 'email', None)
    if not recipient:
        return
    subject = "Your Little Lemon reservation is confirmed"
    body = (
        f"Hi {booking.first_name},\n\n"
        f"Your booking for {booking.guest_number} guest(s) has been received.\n"
        f"Date: {booking.date or 'TBD'}  Time: {booking.time or 'TBD'}\n"
        f"Comment: {booking.comment or '(none)'}\n\n"
        f"We look forward to seeing you!\n"
        f"— Little Lemon"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                  [recipient], fail_silently=True)
    except Exception:
        pass


# ── NEW: BOOKING MANAGEMENT ──────────────────────────────────────────────────────

@login_required
def my_bookings(request):
    """User's own bookings."""
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def booking_edit(request, pk):
    """Edit an existing booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'cancelled':
        messages.error(request, "You cannot edit a cancelled booking.")
        return redirect('my_bookings')
    form = BookingEditForm(request.POST or None, instance=booking)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('my_bookings')
    return render(request, 'booking_edit.html', {'form': form, 'booking': booking})


@login_required
@require_POST
def booking_cancel(request, pk):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect('my_bookings')


# ── NEW: REVIEWS ─────────────────────────────────────────────────────────────────

@login_required
@require_POST
def add_review(request, pk):
    """Submit a review for a menu item."""
    item = get_object_or_404(Menu, pk=pk)
    # prevent duplicate
    if Review.objects.filter(menu_item=item, user=request.user).exists():
        messages.error(request, "You have already reviewed this item.")
        return redirect('menu_detail', pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review           = form.save(commit=False)
        review.menu_item = item
        review.user      = request.user
        review.save()
        messages.success(request, "Review submitted! Thank you.")
    else:
        messages.error(request, "Please fill in the review correctly.")
    return redirect('menu_detail', pk=pk)


@login_required
@require_POST
def delete_review(request, pk):
    """Delete the user's own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    menu_pk = review.menu_item.pk
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect('menu_detail', pk=menu_pk)


# ── NEW: CART ────────────────────────────────────────────────────────────────────

@login_required
def cart_view(request):
    cart = _get_or_create_cart(request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
@require_POST
def cart_add(request, pk):
    """Add 1 of a menu item to cart (or increase qty)."""
    item     = get_object_or_404(Menu, pk=pk, is_available=True)
    cart     = _get_or_create_cart(request.user)
    ci, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        ci.quantity += 1
        ci.save()
    messages.success(request, f"'{item.name}' added to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


@login_required
@require_POST
def cart_remove(request, pk):
    """Remove a cart item entirely."""
    cart = _get_or_create_cart(request.user)
    CartItem.objects.filter(cart=cart, menu_item_id=pk).delete()
    return redirect('cart')


@login_required
@require_POST
def cart_update(request, pk):
    """Update quantity of a cart item."""
    cart = _get_or_create_cart(request.user)
    ci   = get_object_or_404(CartItem, cart=cart, menu_item_id=pk)
    qty  = int(request.POST.get('quantity', 1))
    if qty < 1:
        ci.delete()
    else:
        ci.quantity = qty
        ci.save()
    return redirect('cart')


# ── NEW: CHECKOUT & ORDERS ────────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)
    if not cart.cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    coupon        = None
    discount      = 0
    coupon_form   = CouponForm()
    checkout_form = CheckoutForm()
    total         = cart.total

    # apply coupon from session
    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid():
                discount = total - coupon.apply(total)
            else:
                del request.session['coupon_code']
                coupon = None
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)

    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid():
            # create order
            order = Order.objects.create(
                user   = request.user,
                notes  = checkout_form.cleaned_data['notes'],
                status = 'pending',
            )
            for ci in cart.cart_items.select_related('menu_item'):
                OrderItem.objects.create(
                    order     = order,
                    menu_item = ci.menu_item,
                    quantity  = ci.quantity,
                )
            # use coupon
            if coupon and coupon.is_valid():
                coupon.times_used += 1
                coupon.save()
                request.session.pop('coupon_code', None)
            # award loyalty points
            loyalty = _get_or_create_loyalty(request.user)
            loyalty.add_points(total - discount)
            # clear cart
            cart.cart_items.all().delete()
            messages.success(request,
                f"Order #{order.pk} placed! You earned {int(total - discount)} loyalty points.")
            return redirect('order_detail', pk=order.pk)

    final_total = round(total - discount, 2)
    loyalty     = _get_or_create_loyalty(request.user)
    return render(request, 'checkout.html', {
        'cart':          cart,
        'coupon':        coupon,
        'discount':      discount,
        'total':         total,
        'final_total':   final_total,
        'coupon_form':   coupon_form,
        'checkout_form': checkout_form,
        'loyalty':       loyalty,
    })


@login_required
@require_POST
def apply_coupon(request):
    """Apply coupon code — stores in session."""
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code'].strip().upper()
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid():
                request.session['coupon_code'] = code
                messages.success(request, f"Coupon '{code}' applied!")
            else:
                messages.error(request, "This coupon is expired or no longer valid.")
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon code not found.")
    return redirect('checkout')


@login_required
def order_list(request):
    """All orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__menu_item').order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Detail + live status tracking for one order."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


# ── NEW: LOYALTY ──────────────────────────────────────────────────────────────────

@login_required
def loyalty_dashboard(request):
    loyalty = _get_or_create_loyalty(request.user)
    return render(request, 'loyalty.html', {'loyalty': loyalty})


# ── NEW: ADMIN BOOKING DASHBOARD ──────────────────────────────────────────────────

@login_required
def admin_bookings(request):
    """Staff-only booking management dashboard."""
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('home')
    status   = request.GET.get('status', '')
    bookings = Booking.objects.select_related('user').order_by('-id')
    if status:
        bookings = bookings.filter(status=status)
    return render(request, 'admin_bookings.html', {
        'bookings':        bookings,
        'selected_status': status,
    })


@login_required
@require_POST
def admin_booking_update_status(request, pk):
    """Staff changes booking status."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    booking = get_object_or_404(Booking, pk=pk)
    new_status = request.POST.get('status')
    valid = [s[0] for s in Booking._meta.get_field('status').choices]
    if new_status in valid:
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking #{pk} updated to '{new_status}'.")
    return redirect('admin_bookings')


# ── NEW: ORDER STATUS API (AJAX) ──────────────────────────────────────────────────

@login_required
def order_status_json(request, pk):
    """Returns current order status as JSON for live tracking."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return JsonResponse({
        'status':     order.status,
        'updated_at': order.updated_at.strftime('%H:%M'),
    })
