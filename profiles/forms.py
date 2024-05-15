from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['default_phone_number', 'default_street_address1', 
                  'default_street_address2', 'default_town_or_city', 'default_county', 
                  'default_postcode', 'default_country']

class GardenerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'location', 'about', 'profile_image']