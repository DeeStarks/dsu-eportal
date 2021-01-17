from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.
DEGREE = (
    ("UNDERGRADUATE", "Undergraduate"),
    ("POSTGRADUATE", "Postgraduate"),
)

LEVEL = (
    ("FRESHMAN", "Freshman (100)"),
    ("SOPHOMORE", "Sophomore (200)"),
    ("JUNIOR", "Junior (300)"),
    ("SENIOR", "Senior (400)"),
    ("M-POSTGRADUATE", "Postgraduate (M.Sc)"),
    ("P-POSTGRADUATE", "Postgraduate (Ph.D)")
)

FACULTY = (
    ("SCIENCE", "Faculty of Science"),
    ("ART", "Faculty of Arts"),
)

DEPARTMENT = (
    ("FACULTY OF SCIENCE",
        (
            ("BIOCHEMISTRY", "Biochemistry"),
            ("BOTANY", "Botany"),
            ("CHEMISTRY", "Chemistry"),
            ("COMPUTER_SCIENCE", "Computer Science"),
            ("GEOSCIENCE", "Geoscience"),
            ("MATHEMATICS", "Mathematics"),
            ("MARINE_SCIENCE", "Marine Science"),
            ("MICROBIOLOGY", "Microbiology"),
            ("ZOOLOGY", "Zoology"),
            ("PHYSICS", "Physics"),
        ),
    ),
    ("FACULTY OF ART",
        (
            ("CREATIVE_ART", "Creative Arts"),
            ("ENGLISH", "English"),
            ("EUROPEAN_LANGUAGE", "European Languages & Integration Studies"),
            ("HISTORY", "History & Strategic Studies"),
            ("LINGUISTICS", "Linguistics African Asian Studies"),
            ("PHILOSOPHY", "Philosophy"),
        ),
    ),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_images/')
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    reg_no = models.CharField(max_length=10, null=True, blank=True)
    level = models.CharField(max_length=200, choices=LEVEL, null=True, blank=True)
    faculty = models.CharField(max_length=200, choices=FACULTY, null=True, blank=True)
    department = models.CharField(max_length=200, choices=DEPARTMENT, null=True, blank=True)
    degree = models.CharField(max_length=200, choices=DEGREE, null=True, blank=True)

class StudentCourses(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)