from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):

    bio=forms.CharField(widget=forms.Textarea(attrs={"rows":3 }),required=False)
    class Meta:
        model= get_user_model()
        fields= ('email','username','bio',)
        # exclude=['password',]

class CustomUserChangeForm(UserChangeForm):
    
    bio=forms.CharField(widget=forms.Textarea(attrs={"rows":3 }),required=False)
    class Meta:
        model= get_user_model()
        fields= ('email','username','bio',)
