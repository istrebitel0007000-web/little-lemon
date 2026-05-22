from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Review


# ── EXISTING FORMS (unchanged) ──────────────────────────────────────────────────

class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['first_name', 'last_name', 'guest_number', 'comment', 'date', 'time']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'date':    forms.DateInput(attrs={'type': 'date'}),
            'time':    forms.TimeInput(attrs={'type': 'time'}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ── NEW FORMS ───────────────────────────────────────────────────────────────────

class ReviewForm(forms.ModelForm):
    """Star rating + comment for a menu item."""
    class Meta:
        model  = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating':  forms.Select(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your review...'
            }),
        }


class CouponForm(forms.Form):
    """Apply a coupon code at checkout."""
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter coupon code'}),
    )


class CheckoutForm(forms.Form):
    """Notes field at checkout."""
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Special requests or delivery notes...'
        }),
    )


class BookingEditForm(forms.ModelForm):
    """Allow user to modify their own booking."""
    class Meta:
        model  = Booking
        fields = ['first_name', 'last_name', 'guest_number', 'comment', 'date', 'time']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'date':    forms.DateInput(attrs={'type': 'date'}),
            'time':    forms.TimeInput(attrs={'type': 'time'}),
        }
