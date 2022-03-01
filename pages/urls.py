from django.urls import path
from  .views import HomepageView,AboutpageView
urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('about/',AboutpageView.as_view(), name='about')
]
