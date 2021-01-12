from django.db import models
import datetime
from courses.models import Course


TIMETABLE_TYPE = (
    ('ACADEMIC_CALENDAR', 'Academic Calendar'),
    ('EXAM_TIMETABLE', 'Exam Timetable'),
)

now = datetime.datetime.now()

SESSION = (
    ("YEAR_1", f"{int(now.year)-1}/{now.year} Session"),
    ("YEAR_2", f"{now.year}/{int(now.year)+1} Session"),
)

SEMESTER = (
    ('SEMESTER_1', 'First Semester'),
    ('SEMESTER_2', 'Second Semester'),
)

course_objects = Course.objects.all()
listed__courses = []
for course in course_objects:
    course_alphabets = ''
    for char in course.course_code:
        if char.isalpha():
            course_alphabets+=char
    listed__courses.append(course_alphabets)

registered_courses = []
for course in listed__courses:
    if course not in registered_courses:
        registered_courses.append(course)

COURSES = ()

for course in registered_courses:
    COURSES+=((course.upper(), course),)

# Create your models here.
class Timetable(models.Model):
    type = models.CharField(max_length=100, choices=TIMETABLE_TYPE, null=True)
    session = models.CharField(max_length=50, choices=SESSION, null=True)
    semester = models.CharField(max_length=50, choices=SEMESTER, null=True)
    course = models.CharField(max_length=50, choices=COURSES, null=True)
    file = models.FileField(null=True, upload_to='timetable_files/')
    date_added = models.CharField(max_length=50, null=True)