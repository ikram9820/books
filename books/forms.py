from dataclasses import fields
from django import forms
from .models import Book
class BookCreationForm(forms.ModelForm):
    author= forms.CharField(required=False)
    title= forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3 }),required=False)
    class Meta:
        model=Book
        fields=['title','author','genre','description','store_url','is_visible','pdf']

