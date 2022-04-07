from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

class SignupPageView(generic.CreateView):
    form_class= CustomUserCreationForm
    success_url= reverse_lazy('login')
    template_name= 'registration/signup.html'

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin, generic.UpdateView):
    model= get_user_model()
    fields= ['email','username','bio',]
    success_url= reverse_lazy('my_profile')
    template_name= 'registration/edit_profile.html'


    def test_func(self):
        user= self.get_object()
        if self.request.user == user:
            return True
        return False