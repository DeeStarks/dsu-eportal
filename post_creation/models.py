from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    post = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)
    thumbnail = models.ImageField(upload_to='posts/', default='posts/default.jpg')

    # def get_post(self):
    #     return reverse("post_page", kwargs={"title": self.id})