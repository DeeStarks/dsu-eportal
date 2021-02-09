from .views import semester_and_session
from django.urls import path

urlpatterns = [
    path("session-semester", semester_and_session, name="session and semester")
]