from django import forms
from django.contrib.auth.models import User

from profiles.models import UserProfile


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    gardener = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class GardenerForm(forms.ModelForm):
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'display_name'}))
    location = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'location'}), required=False)
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'profile_image'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'about'}), required=False)

    class Meta:
        model = UserProfile
        fields = ['display_name', 'location', 'profile_image', 'about']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.role == 'GR':
            if not cleaned_data.get('display_name'):
                self.add_error('display_name', 'This field is required.')
            if not cleaned_data.get('location'):
                self.add_error('location', 'This field is required.')
            if not cleaned_data.get('about'):
                self.add_error('about', 'This field is required.')
        return cleaned_data
