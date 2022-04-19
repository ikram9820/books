from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
import uuid
import PyPDF2
import fitz
from books.validators import validate_pdf_size


def cover(url):
    with storage.open(url, "rb") as f:
        with fitz.open(f) as pdf:
            page = pdf.loadPage(0)
            image = page.get_pixmap()
            stream = image.tobytes(output="png")
            return stream


def pages(url):
    with storage.open(url, "rb") as f:
        try:
            readpdf = PyPDF2.PdfFileReader(f)
            return readpdf.numPages
        except:
            return 0


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    pdf = models.FileField(upload_to="book/pdfs", validators=[
                           validate_pdf_size, FileExtensionValidator(allowed_extensions=['pdf'])])
    posted_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to='book/covers', null=True, blank=True)
    download_count = models.IntegerField(default=0)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='book')

    def save(self, *args, **kwargs):
        self.title = str(self.title).title()
        super(Book, self).save(*args, **kwargs)
        try:
            if not self.cover:
                self.cover.save(f'{self.title}.png',
                                ContentFile(cover(self.pdf.name)))
            if not self.pages:
                self.pages = pages(self.pdf.name)
        except Exception as e:
            print("this error is in book model "+str(e))
            book = Book.objects.get(id=self.id)
            book.delete()
            return
        return super(Book, self).save(*args, **kwargs)

    @property
    def size(self):
        mb = 1024*1024
        kb = 1024
        try:
            size = self.pdf.size
        except:
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
    name = models.CharField(max_length=255)
    url = models.URLField()
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='store')


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(get_user_model(
    ), on_delete=models.CASCADE, related_name='favorite', null=True, blank=True, unique=True)


class FavoriteBook(models.Model):
    favorite = models.ForeignKey(
        Favorite, on_delete=models.CASCADE, related_name='favorite_book')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='favorite_book')

    class Meta:
        unique_together = [['favorite', 'book']]
