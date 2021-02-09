from django.urls import path
from .views import profile, update_profile

urlpatterns = [
    path("update/<int:user_id>/<str:user_name>", update_profile, name="update profile"),
    path("<str:group>/<int:user_id>/<str:username>", profile, name="profile"),
]