from django import forms

class SortForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Product Name'),
        ('price', 'Price Low to High'),
        ('-price', 'Price High to Low'),
        ('rating', 'Rating'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))