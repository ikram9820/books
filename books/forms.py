from django import forms
from .models import Book

class BookCreationForm(forms.ModelForm):
    author= forms.CharField(required=False)
    title= forms.CharField(required=False)
    class Meta:
        model=Book
        fields=['title','author','pdf','is_visible']