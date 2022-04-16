from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.conf import settings
import uuid
import PyPDF2
import fitz
from books.validators import validate_pdf_size


def cover(url,title):
    url= '.'+url
    with fitz.open(url) as pdf:
        page=pdf.loadPage(0)
        image= page.get_pixmap()
        name=f"{title}.png"
        name=name.replace(' ','-')
        url= f"{settings.STATIC_URL}/book/covers/{name}"
        image.save(url)
        return url

    
def pages(url):
    url= '.'+url
    file = open(url, 'rb')
    try:
        readpdf = PyPDF2.PdfFileReader(file)
        return readpdf.numPages
    except :
        return 0



class Book(models.Model):
    id= models.UUIDField(primary_key=True,default= uuid.uuid4,editable= False)
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200,blank=True ,null=True)
    pdf= models.FileField(upload_to="book/pdfs",validators=[validate_pdf_size,FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at= models.DateTimeField(auto_now_add=True)
    is_visible= models.BooleanField(default=True)
    pages=models.IntegerField(null=True,blank=True)
    cover_url=models.CharField(max_length=220,null=True,blank=True)
    download_count= models.IntegerField(default=0)
    user= models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='book')

    def save(self,*args,**kwargs ):
        self.title= str(self.title).title()
        super(Book,self).save(*args,**kwargs)
        try:
            if not self.cover_url:
                self.cover_url= cover(self.pdf.url,self.title)
            if not self.pages:
                self.pages=pages(self.pdf.url)
        except Exception as e :
            print("this the error in book model "+str(e))
            book= Book.objects.get(id =self.id)
            book.delete()
            return
        return super(Book,self).save(*args,**kwargs) 

    @property
    def size(self):
        mb=1024*1024
        kb=1024
        try:
            size=self.pdf.size
        except :
            return
        if size > mb:
            return f"{'{:.2f}'.format(size/mb)} mb"
        elif size > kb:
            return f"{'{:.2f}'.format(size/kb)} kb"
        else:
            return f"{'{:.2f}'.format(size)} bytes"   

    def __str__(self):
        try:
            return self.title
        except:
            return

    def get_absolute_url(self):
        try:
            return reverse("book_detail", args=[str(self.id)])
        except:
            return


class Store(models.Model):
    name=models.CharField(max_length=255)
    url=models.URLField()
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='store')


class Favorite(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False)
    at= models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='favorite',null=True,blank=True,unique=True)

class FavoriteBook(models.Model):
    favorite=models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite_book')
    book= models.ForeignKey(Book,on_delete=models.CASCADE,related_name='favorite_book')
    
    class Meta:
        unique_together= [['favorite','book']]
