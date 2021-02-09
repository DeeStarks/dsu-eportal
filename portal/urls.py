from django.urls import path
from .views import students, staff, confirm_user_delete, delete_user, redirect_user

urlpatterns = [
    path("students/", students, name="students"),
    path("staff/", staff, name="staff"),
    path("<str:group>/delete/<str:username>", confirm_user_delete, name="confirm delete user"),
    path("<str:group>/delete/confirm/<str:username>", delete_user, name="delete user"),
    path("redirect/<int:user_id>", redirect_user, name="redirect user")
]