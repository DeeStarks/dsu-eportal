from django.contrib import admin
from .models import ContinousAssessment, StudentGrade, UploadedScoresheets, CarryOver

# Register your models here.
admin.site.register(ContinousAssessment)
admin.site.register(StudentGrade)
admin.site.register(UploadedScoresheets)
admin.site.register(CarryOver)
