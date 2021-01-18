from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myapp.decorators import user_group
from courses.models import CourseAllocation
import io
import os
from pathlib import Path
import csv
from session_semester.models import SessionAndSemester
from user_profile.models import StudentCourses, UserProfile, DEPARTMENT
from courses.models import Course

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['staff'])
def scoresheet(request, *args, **kwargs):
    staff_object = User.objects.get(username=request.user.username)
    courses_allocated = CourseAllocation.objects.filter(staff_name=staff_object)
    context = {
        'courses': courses_allocated.order_by('course__course_code')
    }
    return render(request, 'lecturer_panel/scoresheet.html', context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['staff'])
def scoresheet_download(request, course_code):
    course = Course.objects.get(course_code=course_code)
    student_course_objects = StudentCourses.objects.filter(courses=course)
    students_taking_courses = []
    course_level = ''

    for student_object in student_course_objects:
        user = User.objects.get(username=student_object.user.username)
        level = UserProfile.objects.get(user=user).level

        for num in range(100, 200):
            if str(num) in course_code and level == "FRESHMAN":
                students_taking_courses.append(user)
        for num in range(200, 300):
            if str(num) in course_code and level == "SOPHOMORE":
                students_taking_courses.append(user)
        for num in range(300, 400):
            if str(num) in course_code and level == "JUNIOR":
                students_taking_courses.append(user)
        for num in range(400, 500):
            if str(num) in course_code and level == "SENIOR":
                students_taking_courses.append(user)
                
    if len(students_taking_courses) >= 1:
        course_level = UserProfile.objects.get(user=students_taking_courses[0]).get_level_display

    if course_level != '':
        staff = User.objects.get(username=request.user.username)
        session__semester = SessionAndSemester.objects.get(id=1)

        header = [
            ['DEESTARKS UNIVERSITY'],
            [f'{session__semester.get_session_display()}'],
            [f'{session__semester.get_semester_display()}'],
            [f'{course.course_code} ({course.course_title}) - {course.course_unit} unit(s)'],
            [f'{course_level()} Level']
        ]

        content = [
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', 'Continous Assessment', '', '', '', '', 'Examination', '', '', '', '', ],
            ['', '', '', 'Att.', 'ASSIGN.', 'Quiz', 'Test',  'Total', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Total'],
            ['S/N', 'NAMES', 'MATRIC NO', '5', '10', '10', '15', '40', '15', '15', '15', '15', '15', '60']
        ]
        
        for index, student in enumerate(students_taking_courses):
            content.append([index+1, student.get_full_name(), student.username, '', '', '', '', '', '', '', '', '', '', ''])

        # Creating a CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{session__semester.get_session_display()}-{session__semester.get_semester_display()}-{course_code}-scoresheet.csv"'

        # Writing into the created CSV file
        writer = csv.writer(response)
        writer.writerows(header)
        writer.writerows(content)
        return response
    else:
        return render(request, 'lecturer_panel/no_student.html')
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['staff'])
def scoresheet_upload(request, course_code):
    BASE_DIR = Path(__file__).resolve().parent.parent

    # with open(os.path.join(BASE_DIR, 'media/assessment_files/scoresheet_templates/template_1.csv'), 'w') as scoresheet:
        # write_sheet = csv.writer()

    context = {
        'course_code': course_code
    }
    return render(request, "lecturer_panel/upload.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def mastersheet(request, *args, **kwargs):
    all_departments = []
    for department_obj in DEPARTMENT:
        for departments in department_obj[1]:
            all_departments.append(departments[1])
    print(all_departments)
    
    context = {
        
    }
    return render(request, 'admin_panel/mastersheet.html', context)