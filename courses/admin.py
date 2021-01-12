from django.contrib import admin
from .models import Course, CourseAllocation

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseAllocation)