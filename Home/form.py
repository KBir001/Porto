from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('C', 'COD')
)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class PriceForm(forms.Form):
    min_price = forms.FloatField(widget = forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Min'
        
    }))
    max_price = forms.FloatField(widget = forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Max'
    }))

class SearchForm(forms.Form):
    data=forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Search.....',
        'type':'search',
        'name':'q',
        'id':'q'
    }))

class CouponForm(forms.Form):
    coupon = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Enter discount code'
    }))

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St',
        'id': 'address'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite',
        'id': 'address-2'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',

        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'pattern':'[0-9]{6}'
    }))
    contact = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'contact',
        'placeholder':'10 digit mobile number',
        'pattern':'[789][0-9]{9}'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
