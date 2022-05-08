from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from books.validators import validate_pdf_size
import uuid

    
class Genre(models.Model):
    name = models.CharField(max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    pdf = models.FileField(upload_to="book/pdfs", validators=[
                           validate_pdf_size, FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    pages = models.IntegerField(null=True, blank=True)
    store_url = models.URLField(null=True, blank=True)
    cover = models.ImageField(upload_to='book/covers', null=True, blank=True)
    download_count = models.IntegerField(default=0)
    genre = models.ForeignKey(Genre,on_delete=models.PROTECT,related_name='book',null=True,blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='book')


    @property
    def size(self):
        kb = 1024
        size = self.pdf.size
        if size > (kb*kb):
            return f"{int(size/(kb*kb))} mb"
        elif size > kb:
            return f"{int(size/kb)} kb"
        else:
            return f"{int(size)} b"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])




class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='favorite', null=True, blank=True, unique=True)

class FavoriteBook(models.Model):
    favorite = models.ForeignKey(
        Favorite, on_delete=models.CASCADE, related_name='favorite_book')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='favorite_book')

    class Meta:
        unique_together = [['favorite', 'book']]
