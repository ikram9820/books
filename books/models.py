from email.policy import default
from uuid import UUID
from django.db import models
from django.forms import UUIDField
from django.urls import reverse
import uuid

class Book(models.Model):
    id= models.UUIDField(primary_key=True,default= uuid.uuid4,editable= False)
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200)
    price= models.DecimalField(max_digits=6,decimal_places=2)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])

    
    

