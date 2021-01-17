from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GROUPING = (
    ("CORE", "Core"),
    ("ELECTIVE", "Elective"),
    ("GENERAL STUDIES", "General Studies")
)


class Course(models.Model):
    course_code = models.CharField(max_length=150, null=True, blank=True)
    course_title = models.CharField(max_length=150, null=True, blank=True)
    course_unit = models.CharField(max_length=150, null=True, blank=True)
    grouping = models.CharField(max_length=100, choices=GROUPING, default=None)
    department = models.CharField(max_length=150, null=True, blank=True)

class CourseAllocation(models.Model):
    
    staff_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, null=True)