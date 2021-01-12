from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group

# Create your views here.
@login_required(login_url='authentication')
def library(request):
    queryset = Book.objects.all()
    context = {
        'objects': reversed(queryset)
    }
    return render(request, "library.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def update_library(request):
    queryset = Book.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        thumbnail = None
        book = None
        if request.FILES:
            book = request.FILES.get('book')
            thumbnail = request.FILES.get('thumbnail')

        Book.objects.create(
            filename=title,
            thumbnail=thumbnail,
            file=book
        )
    context = {
        'books': reversed(queryset)
    }
    return render(request, "admin_panel/update-library.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def remove_book(request, book_id, *args, **kwargs):
    book = Book.objects.get(id=book_id)
    context = {
        'book': book
    }
    return render(request, "admin_panel/remove-book.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def confirm_book_removal(request, book_id, *args, **kwargs):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('update library')