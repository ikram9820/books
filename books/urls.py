from django.urls import path
from .views import *

urlpatterns = [
    path('',BookListView.as_view(),name='book_list'),
    path('<uuid:pk>/',BookDetailView.as_view(),name='book_detail'),
    path('<uuid:pk>/delete/',BookDeleteView.as_view(),name='book_delete'),
    path('<uuid:pk>/update/',BookUpdateView.as_view(),name='book_edit'),
     path('<uuid:pk>/update_visibility/',BookVisibilityUpdateView.as_view(),name='book_visibility'),
    path('create/',BookCreateView.as_view(),name='add_book'),
    path('<uuid:pk>/add_to_favorite/',add_book_to_fav,name='add_book_to_fav'),
    path('favorite/',get_fav_book_list,name='favorite'),
    path('profile/',MyProfileListView.as_view(),name= 'my_profile'),
    path('search/',SearchResultsListView.as_view(),name='search_results'),
    path('<str:username>/',ProfileListView.as_view(),name='user_profile'),
]
