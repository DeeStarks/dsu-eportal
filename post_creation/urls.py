from django.urls import path
from .views import create_post, confirm_delete, delete_post

urlpatterns = [
    path("post/create", create_post, name="update post"),
    path("post/delete/<int:post_id>", confirm_delete, name="confirm delete"),
    path("post/delete/<int:post_id>/<str:title>", delete_post, name="delete post")
]