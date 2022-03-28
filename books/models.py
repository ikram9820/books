from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import uuid
import PyPDF2
import fitz
from config.settings import common
from books.validators import validate_pdf_size

class Book(models.Model):
    id= models.UUIDField(primary_key=True,default= uuid.uuid4,editable= False)
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200,blank=True ,null=True)
    pdf= models.FileField(upload_to="book/pdfs",validators=[validate_pdf_size,FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at= models.DateTimeField(auto_now_add=True)
    is_visible= models.BooleanField(default=True)
    download_count= models.IntegerField(default=0)
    user= models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='book')

    def save(self,*args,**kwargs ):
        self.title= str(self.title).title()
        return super(Book,self).save(*args,**kwargs)

    @property
    def cover(self):
        url= self.pdf.url
        pdf= fitz.open(url)
        print(self.pdf.url)
        page=pdf.loadPage(0)
        image= page.get_pixmap()
        name=f"{self.title}.png"
        name=name.replace(' ','-')
        url= f"media/book/covers/{name}"
        image.save(url)
        return url

    @property
    def pages(self):
        url= '.'+self.pdf.url
        file = open(url, 'rb')
        try:
            readpdf = PyPDF2.PdfFileReader(file)
            return readpdf.numPages
        except :
            return 0

    # @property       
    # def pages(self):
    #     output = check_output(["pdfinfo", self.pdf.url]).decode()
    #     pages_line = [line for line in output.splitlines() if "Pages:" in line][0]
    #     num_pages = int(pages_line.split(":")[1])
    #     return num_pages



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
