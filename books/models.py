from unicodedata import decimal
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid

class Book(models.Model):
    id= models.UUIDField(primary_key=True,default= uuid.uuid4,editable= False)
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200,blank=True ,null=True)
    pdf= models.FileField(upload_to='pdfs/')
    posted_at= models.DateTimeField(auto_now_add=True)
    is_visible= models.BooleanField(default=True)
    download_count= models.IntegerField(default=0)
    discription= models.TextField(null=True,blank=True)
    user= models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='book')

    @property
    def size(self):
        size= self.pdf.size
        if(size> 1024*1024 ):
            size=size/(1024*1024)
            size="{:.2f}".format(size)
            return f'{size} mb'
        size=size/(1024)
        size="{:.2f}".format(size)
        return f'{size/1024} kb'


    class Meta:
        permissions= [
            ('special_status','Can read all books')
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class Store(models.Model):
    name=models.CharField(max_length=255)
    url=models.URLField()
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='store')

class Review(models.Model):
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name='review')
    review= models.CharField(max_length=255)
    rating= models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    author= models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='review')

    def __str__(self):
        return self.review
    class Meta:
        unique_together= [['book','author']]


class Favorite(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    at= models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='favorite')

class FavoriteBooks(models.Model):
    favorite=models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite_book')
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name='favorite_book')
    
    class Meta:
        unique_together= [['favorite','book']]
