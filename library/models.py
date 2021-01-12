from django.db import models

# Create your models here.
class Book(models.Model):
    filename = models.CharField(max_length=200, default="Title")
    file = models.FileField(upload_to="books/")
    thumbnail = models.ImageField(upload_to="books/thumbnails/", default="books/thumbnails/book.jpg")