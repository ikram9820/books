from django.contrib import admin
from .models import Book,Store,Favorite,FavoriteBook


class StoreInline(admin.TabularInline):
    model=Store

class BookAdmin(admin.ModelAdmin):
    inlines=[StoreInline]
    list_display= ('title','user','author','is_visible','size')
    
admin.site.register(Book,BookAdmin)



class FavoriteBookInline(admin.TabularInline):
    model=FavoriteBook

class FavoriteAdmin(admin.ModelAdmin):
    inlines=[FavoriteBookInline]
    list_display= ['id','user','at']
    
admin.site.register(Favorite,FavoriteAdmin)