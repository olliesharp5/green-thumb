from django.shortcuts import render, redirect
from django.contrib.auth import login

from profiles.models import UserProfile, Wishlist
from .forms import RegistrationForm, GardenerForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        gardener_form = GardenerForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user_form.cleaned_data['gardener']:
                if gardener_form.is_valid():
                    gardener_profile = gardener_form.save(commit=False)
                    gardener_profile.user = user
                    gardener_profile.role = 'GR'
                    gardener_profile.save()
                    Wishlist.objects.create(user=gardener_profile)  # Create Wishlist for gardener
                else:
                    # Handle the case where the gardener form is not valid
                    return render(request, 'accounts/register.html', {'user_form': user_form, 'gardener_form': gardener_form})
            else:
                user_profile = UserProfile.objects.create(user=user, role='RU')
                Wishlist.objects.create(user=user_profile) 
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            return redirect('home')
    else:
        user_form = RegistrationForm()
        gardener_form = GardenerForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'gardener_form': gardener_form})