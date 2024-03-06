from django import forms
from stripe import Review
from .models import ProductImages, ProductReview, Vendor

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
class ProductReviewForm(forms.ModelForm):
    subject=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'write your review\'s subject '}))
    review=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'write your review'}))
    class Meta:
        model =  ProductReview
        fields = ['subject', 'review','rating']


class ProductImageForm(forms.Form):
    selected_images = forms.ModelMultipleChoiceField(
        queryset=ProductImages.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class EditProductImageForm(forms.Form):
    images = forms.ImageField(
        label='Nouvelles images',
        # widget=forms.FileInput(attrs={'multiple': True}),
    )