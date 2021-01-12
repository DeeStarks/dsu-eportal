from .views import update_library, remove_book, confirm_book_removal
from django.urls import path

urlpatterns = [
    path("update", update_library, name="update library"),
    path("remove/<int:book_id>/<str:filename>", remove_book, name="remove book"),
    path("remove/confirm/<int:book_id>", confirm_book_removal, name="confirm book remove"),
]