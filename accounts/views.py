from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm

class SignupPageView(generic.CreateView):
    form_class= CustomUserCreationForm
    success_url= reverse_lazy('login')
    template_name= 'registration/signup.html'

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    pass