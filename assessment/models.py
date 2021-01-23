from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.
class ContinousAssessment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    ca_total = models.IntegerField(null=True, blank=True)
    exam_total = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    grading_point = models.IntegerField(null=True, blank=True)
    quality_point = models.IntegerField(null=True, blank=True)
    session = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=100, null=True, blank=True)
    
class StudentGrade(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=100, null=True, blank=True)
    tcu = models.IntegerField(null=True, blank=True)
    gpa = models.CharField(max_length=100, null=True, blank=True)
    cgpa = models.CharField(max_length=100, null=True, blank=True)

# Very Important
class UploadedScoresheets(models.Model):
    sheet_name = models.CharField(max_length=100, null=True, blank=True)
