from django.urls import path
from .views import all_courses, add_course, remove_course, confirm_remove, allocate_course, allocated_list

urlpatterns = [
    path("courses/", all_courses, name="all courses"),
    path("courses/add", add_course, name="add course"),
    path("courses/remove/<int:course_id>", remove_course, name="remove course"),
    path("courses/remove/confirm/<int:course_id>", confirm_remove, name="confirm course remove"),
    path("courses/allocate", allocate_course, name="allocate course"),
    path("courses/allocations", allocated_list, name="allocated list"),
]