from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
import datetime
from courses.models import Course
from .models import Timetable
import datetime

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def timetable(request):
    timetable__queryset = Timetable.objects.all()
    now = datetime.datetime.now()
    date = now.strftime('%b %d, %Y,')
    context = {
        'timetable__queryset': timetable__queryset.order_by('-id'),
        'date': date,
        'month': now.strftime('%b'),
        'day': now.strftime('%d,'),
        'year': now.strftime('%Y,')
    }
    return render(request, "table.html",context)


@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def update_timetable(request):
    now = datetime.datetime.now()
    message = ''

    # Getting all available courses
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

    courses = []

    for course in registered_courses:
        courses.append(course)
    if request.method == 'POST':
        table__type = request.POST.get('table_type')
        session = request.POST.get('session')
        semester = request.POST.get('semester')
        course = request.POST.get('course')
        file = None
        now = datetime.datetime.now()
        date__added = now.strftime('%b %d, %Y, %I:%M %p')
        if request.FILES:
            file = request.FILES.get('timetable_file')
            
        if table__type == 'ACADEMIC_CALENDAR':
            Timetable.objects.create(
                type=table__type,
                session=session,
                date_added=date__added,
                file=file
            )
            message = "Timetable uploaded!"
        elif table__type == 'EXAM_TIMETABLE':
            Timetable.objects.create(
                type=table__type,
                course=course,
                semester=semester,
                session=session,
                date_added=date__added,
                file=file
            )
            message = "Timetable uploaded!"
    context = {
        "year_1": f"{int(now.year)-1}/{now.year} Session",
        "year_2": f"{now.year}/{int(now.year)+1} Session",
        "all_courses": courses,
        "success": message
    }
    return render(request, "admin_panel/update-timetable.html",context)

