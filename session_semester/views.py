from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from .models import SessionAndSemester
from django.contrib.auth.models import User
from user_profile.models import UserProfile

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def semester_and_session(request, *args, **kwargs):
    now = datetime.datetime.now()
    ss_object = SessionAndSemester.objects.all()
    current_session = None
    for object in ss_object:
        current_session = object.get_session_display()

    message = ''
    if request.method == "POST":
        semester = request.POST.get("semester")
        session = request.POST.get("session")
        session__semester = None
        for object in ss_object:
            session__semester = object

        if session__semester:
            session__semester.semester = semester
            session__semester.session = session
            session__semester.save()
        else:
            SessionAndSemester.objects.create(
                semester=semester,
                session=session
            )
        message = "Settings Saved!"

        current_year = [int(year) for year in current_session.split(' ')[0].split('/')]
        new_year = [int(year) for year in SessionAndSemester.objects.get(id=1).get_session_display().split(' ')[0].split('/')]
        if (new_year[0] > current_year[0]) and (new_year[1] > current_year[1]):
            for student in User.objects.filter(groups__name="students"):
                student_profile = UserProfile.objects.get(user=student)
                if student_profile.level == "FRESHMAN":
                    student_profile.level = "SOPHOMORE"
                elif student_profile.level == "SOPHOMORE":
                    student_profile.level = "JUNIOR"
                elif student_profile.level == "JUNIOR":
                    student_profile.level = "SENIOR"
                elif student_profile.level == "SENIOR":
                    student.delete()

                student_profile.save()
        
    context = {
        "session__semester": SessionAndSemester.objects.get(id=1),
        "year_1": f"{int(now.year)-1}/{now.year} Session",
        "year_2": f"{now.year}/{int(now.year)+1} Session",
        "year_3": f"{int(now.year)+1}/{int(now.year)+2} Session",
        "year_4": f"{int(now.year)+2}/{int(now.year)+3} Session",
        "success": message,
    }
    return render(request, "admin_panel/semester-session.html", context)