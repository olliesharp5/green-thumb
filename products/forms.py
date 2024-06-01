from django import forms
from django.core.validators import MinValueValidator

from .models import Product, Category, Review


class SortForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Product Name'),
        ('price', 'Price Low to High'),
        ('-price', 'Price High to Low'),
        ('recent', 'Recently Added'),
        ('highest_rating', 'Highest Rating'),
        ('best_selling', 'Best Selling'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, widget=forms.Select(attrs={'onchange': 'this.form.submit();','class': 'sort-form'}))


class ProductForm(forms.ModelForm):
    sku = forms.CharField(label='SKU', widget=forms.TextInput(attrs={'class': 'form-control'}))
    has_size = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    price = forms.DecimalField(label='Price ($)', validators=[MinValueValidator(0.1)], widget=forms.TextInput(attrs={'class': 'form-control', 'oninput': 'this.value = this.value.replace(/[^0-9.]/g, "").replace(/(\..*)\./g, "$1");'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'has_size', 'price', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    class Meta:
        model = Review
        fields = ['title', 'rating', 'text']