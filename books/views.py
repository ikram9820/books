from pickle import TRUE
from pydoc import classify_class_attrs
from re import template
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Book

class BookListView(ListView):
    model= Book
    template_name= 'books/book_list.html'
    context_object_name= 'books'
    paginate_by=2

    def get_queryset(self):
        return Book.objects.filter(is_visible=True).order_by('-posted_at')

class BookDetailView(DetailView):
    model= Book
    template_name='books/book_detail.html'
    context_object_name= 'book'
    login_url= 'login'

class BookCreateView(LoginRequiredMixin,CreateView):
    model= Book
    template_name= 'books/book_form.html'
    fields= ['title','author','pdf','is_visible','discription']
    success_url= '/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model= Book
    template_name= "books/book_form.html"
    fields= ['title','author','pdf','is_visible','discription']
    success_url= '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book= self.get_object()
        if self.request.user == book.user:
            return True
        return False


class BookVisibilityUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model= Book
    template_name= "books/book_form.html"
    fields= ['is_visible']
    success_url= '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book= self.get_object()
        if self.request.user == book.user:
            return True
        return False
class BookDelteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model= Book
    success_url= '/'
    template_name='books/delete_book.html'

    def test_func(self):
        book= self.get_object()
        if self.request.user == book.user:
            return True
        return False



class FavoriteCreateView(CreateView):
    pass

class FavoriteDetailView(DetailView):
    pass

class FavItemCreateView(CreateView):
    pass

class FavItemListView(ListView):
    pass

class ProfileListView(ListView):
    model=Book
    template_name='profile/profile.html'
    context_object_name='books'
    paginate_by=2

    def get_context_data(self, **kwargs):
        context= super(ProfileListView,self).get_context_data(**kwargs)
        if self.kwargs.get('username'):
            context['profile_user']= get_object_or_404(get_user_model(), username= self.kwargs.get('username'))
        elif self.request.user.is_authenticated:
            context['profile_user']= self.request.user
        
        return context

    def get_queryset(self):
        if self.kwargs.get('username'):
            user= get_object_or_404(get_user_model(), username= self.kwargs.get('username'))
        elif self.request.user.is_authenticated:
            user=self.request.user
        else:
            user= None

        return Book.objects.filter(Q(user=user)& Q(is_visible=True)).order_by('-posted_at')
    
class MyProfileListView(ListView):
    model=Book
    template_name='profile/my_profile.html'
    context_object_name='books'
    paginate_by=2
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user=self.request.user
        else:
            user= None

        return Book.objects.filter(user=user).order_by('-posted_at')
    
class SearchResultsListView(ListView):
    model= Book
    context_object_name='books'
    tempalte_name='books/search_results.html'   
    def get_queryset(self):
        query= self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query) & Q(is_visible=True)).order_by('-posted_at')









