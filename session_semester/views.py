from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from .models import SessionAndSemester

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def semester_and_session(request, *args, **kwargs):
    now = datetime.datetime.now()
    message = ''
    if request.method == "POST":
        semester = request.POST.get("semester")
        session = request.POST.get("session")

        session__semester = SessionAndSemester.objects.get(id=1)

        session__semester.semester = semester
        session__semester.session = session
        session__semester.save()
        message = "Settings Saved!"
    context = {
        "session__semester": SessionAndSemester.objects.get(id=1),
        "year_1": f"{int(now.year)-1}/{now.year} Session",
        "year_2": f"{now.year}/{int(now.year)+1} Session",
        "year_3": f"{int(now.year)+1}/{int(now.year)+2} Session",
        "year_4": f"{int(now.year)+2}/{int(now.year)+3} Session",
        "success": message,
    }
    return render(request, "admin_panel/semester-session.html", context)