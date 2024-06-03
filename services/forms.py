from django import forms

from profiles.models import UserProfile
from .models import GardenerFeedback


class GardenerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.display_name

class GardenerFeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    gardener = GardenerChoiceField(queryset=UserProfile.objects.filter(role='GR'))
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    class Meta:
        model = GardenerFeedback
        fields = ['gardener', 'title', 'message', 'rating']