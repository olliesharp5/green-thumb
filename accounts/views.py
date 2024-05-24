from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from profiles.models import UserProfile, Wishlist
from .forms import RegistrationForm, GardenerForm
from django.contrib import messages

def register(request):
    """
    Handles the registration of a new user and their corresponding profile. If the user opts to 
    register as a gardener, additional information is collected and saved.

    **Context**

    ``user_form``
    An instance of `RegistrationForm` to handle user registration data.

    ``gardener_form``
    An instance of `GardenerForm` to handle gardener profile data if the user registers as a gardener.

    **Methods**

    ``register(request)``
    Handles both GET and POST requests for user registration. On a POST request, it processes 
    the submitted registration forms, validates them, and creates the corresponding user and 
    profile instances in the database. If any form errors are encountered, it renders the 
    registration form again with error messages.

    **Template:**

    :template:`accounts/register.html`
    """
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        gardener_form = GardenerForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            if user_form.cleaned_data['gardener']:
                gardener_form.instance.role = 'GR'  # Set role before validation
                gardener_form.instance.user = user  # Associate user with gardener profile
                if gardener_form.is_valid():
                    with transaction.atomic():
                        gardener_profile = gardener_form.save(commit=False)
                        gardener_profile.user = user
                        gardener_profile.role = 'GR'
                        gardener_profile.save()
                        Wishlist.objects.create(user=gardener_profile)
                        user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, 'Please correct the error below.')
                    return render(request, 'accounts/register.html', {
                        'user_form': user_form,
                        'gardener_form': gardener_form
                    })
            else:
                with transaction.atomic():
                    user_profile = UserProfile.objects.create(user=user, role='RU')
                    Wishlist.objects.create(user=user_profile)
                    user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                    login(request, user)
                    return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'accounts/register.html', {
                'user_form': user_form,
                'gardener_form': gardener_form
            })
    else:
        user_form = RegistrationForm()
        gardener_form = GardenerForm()
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'gardener_form': gardener_form
    })

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        gardener_form = GardenerForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            if user_form.cleaned_data['gardener']:
                gardener_form.instance.role = 'GR'  # Set role before validation
                gardener_form.instance.user = user  # Associate user with gardener profile
                if gardener_form.is_valid():
                    with transaction.atomic():
                        gardener_profile = gardener_form.save(commit=False)
                        gardener_profile.user = user
                        gardener_profile.role = 'GR'
                        gardener_profile.save()
                        Wishlist.objects.create(user=gardener_profile)
                        user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, 'Please correct the error below.')
                    return render(request, 'accounts/register.html', {
                        'user_form': user_form,
                        'gardener_form': gardener_form
                    })
            else:
                with transaction.atomic():
                    user_profile = UserProfile.objects.create(user=user, role='RU')
                    Wishlist.objects.create(user=user_profile)
                    user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                    login(request, user)
                    return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'accounts/register.html', {
                'user_form': user_form,
                'gardener_form': gardener_form
            })
    else:
        user_form = RegistrationForm()
        gardener_form = GardenerForm()
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'gardener_form': gardener_form
    })
