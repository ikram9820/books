from django import forms
from .models import Book

class BookCreationForm(forms.ModelForm):
    class Meta:
        model:Book
        fields=['title','author','pdf','size','is_visible','description','user']