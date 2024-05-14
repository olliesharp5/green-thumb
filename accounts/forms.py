from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    gardener = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class GardenerForm(forms.ModelForm):
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'id': 'display_name'}))
    location = forms.CharField(widget=forms.Textarea(attrs={'id': 'location'}), required=False)
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'id': 'profile_image'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'id': 'about'}), required=False)

    class Meta:
        model = UserProfile
        fields = ['display_name', 'location', 'profile_image', 'about']