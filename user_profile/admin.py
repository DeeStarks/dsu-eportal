from django.contrib import admin
from .models import UserProfile, StudentCourses

# Register your models here.
admin.site.register(StudentCourses)
admin.site.register(UserProfile)