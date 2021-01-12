from django.forms import ModelForm
from .models import Post

class PostCreation(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'