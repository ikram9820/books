import imp
import django
from .views import SignupPageView
from django.urls import path

urlpatterns = [
    path('signup/',SignupPageView.as_view(),name='signup')
]
