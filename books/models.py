from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid
import os
import PyPDF2

class Book(models.Model):
    id= models.UUIDField(primary_key=True,default= uuid.uuid4,editable= False)
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200,blank=True ,null=True)
    pdf= models.FileField(upload_to=f'book/pdfs/')
    cover=models.ImageField(upload_to=f'book/covers/',blank=True ,null=True)
    posted_at= models.DateTimeField(auto_now_add=True)
    is_visible= models.BooleanField(default=True)
    download_count= models.IntegerField(default=0)
    user= models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='book')

    @property
    def size(self):
        mb=1024*1024
        kb=1024
        size=self.pdf.size
        if size > mb:
            return f"{'{:.2f}'.format(size/mb)} mb"
        elif size > kb:
            return f"{'{:.2f}'.format(size/kb)} kb"
        else:
            return f"{'{:.2f}'.format(size)} bytes"

    @property
    def pages(self):
        url= '.'+self.pdf.url
        with open(url,'rb') as pdf:
            reder= PyPDF2.PdfFileReader(pdf)
            return reder.numPages


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])


class Store(models.Model):
    name=models.CharField(max_length=255)
    url=models.URLField()
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='store')


class Favorite(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    at= models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='favorite',null=True,blank=True)

class FavoriteBook(models.Model):
    favorite=models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite_book')
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name='favorite_book')
    
    class Meta:
        unique_together= [['favorite','book']]
