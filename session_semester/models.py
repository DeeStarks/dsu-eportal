from django.db import models
import datetime

SEMESTER = (
    ("FIRST_SEMESTER", "First Semester"),
    ("SECOND_SEMESTER", "Second Semester")
)

now = datetime.datetime.now()

SESSION = (
    ("YEAR_1", f"{int(now.year)-1}/{now.year} Session"),
    ("YEAR_2", f"{now.year}/{int(now.year)+1} Session"),
    ("YEAR_3", f"{int(now.year)+1}/{int(now.year)+2} Session"),
    ("YEAR_4", f"{int(now.year)+2}/{int(now.year)+3} Session")
)

# Create your models here.
class SessionAndSemester(models.Model):
    semester = models.CharField(max_length=50, choices=SEMESTER, null=True)
    session = models.CharField(max_length=50, choices=SESSION, null=True)
