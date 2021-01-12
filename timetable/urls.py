from .views import update_timetable
from django.urls import path

urlpatterns = [
    path('update', update_timetable, name="update timetable")
]