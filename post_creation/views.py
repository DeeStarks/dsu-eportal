from django.shortcuts import render, redirect
from .models import Post
from datetime import date
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from .forms import PostCreation
from django.core.files.storage import FileSystemStorage
import random

# Create your views here.
@login_required(login_url='authentication')
def posts(request, post_id, title):
    year = date.today().year
    queryset = Post.objects.get(id=post_id)
    all_queryset = Post.objects.all()
    return_set = []
    for i in range(10):
        a = random.choice(all_queryset)
        if a not in return_set:
            return_set.append(a)

    context = {
        'year': int(year),
        'objects': queryset,
        'all_set': return_set
    }
    return render(request, "post.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def create_post(request):
    success = ''
    all_queryset = Post.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        post = request.POST.get('body')
        if request.FILES:
            post_cover = request.FILES['thumbnail']

        Post.objects.create(title=title, post=post, thumbnail=post_cover)
        success = f"Post added successfully."

    context = {
        'all_set': reversed(all_queryset),
        'success': success
    }
    return render(request, "admin_panel/update-news.html", context)


@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def confirm_delete(request, post_id):
    queryset = Post.objects.get(id=post_id)
    context = {
        'object': queryset
    }
    return render(request, "admin_panel/delete_post.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])  
def delete_post(request, post_id, title):
    Post.objects.filter(id=post_id).delete()
    return redirect('update post')