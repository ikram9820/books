from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/',include('django.contrib.auth.urls')),
    # path('accounts/',include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('',include('pages.urls')),
    path('books/',include('books.urls')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)