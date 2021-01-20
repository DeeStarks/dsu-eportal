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
            [f'{course_level()} Level'],
            [f'Scoresheet by: {request.user.get_full_name()}']
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
    message = {
        'outcome': '',
        'message': '',
        'color': ''
    }
    
    students_grades = {}

    if request.method == "POST":
        sheet = None
        if request.FILES:
            sheet = request.FILES.get('sheet')

        if sheet != None:
            if sheet.name.endswith(".csv"):
                try:
                    sheet_name = sheet.name.split("-")
                    scoresheet_session = sheet_name[0].replace("_", "/")
                    scoresheet_semester = sheet_name[1]
                    scoresheet_course_code = sheet_name[2]
                    if scoresheet_course_code != course_code:
                        message['outcome'] = "Failed!"
                        message['message'] = f"You uploaded a scoresheet with course code - {scoresheet_course_code}, instead of {course_code}"
                        message['color'] = "red"
                    else:
                        sheet_decode = io.TextIOWrapper(sheet.file, encoding='utf-8 ', errors='replace')
                        sheet_reader = csv.reader(sheet_decode, delimiter=",")
                        main_sheet = [sheet for sheet in sheet_reader]

                        if not main_sheet:
                            message['outcome'] = "Failed!"
                            message['message'] = "The scoresheet you uploaded contains no students!"
                            message['color'] = "red"
                        else:
                            for index, row in enumerate(main_sheet):
                                if row[0].isnumeric():
                                    if int(row[0]) == 1:
                                        recorded_students = [grade for grade in main_sheet[index:]]
                                        for grade in recorded_students:
                                            if grade[0].isnumeric():
                                                students_grades[grade[2]] = {}
                                                students_grades[grade[2]]["name"] = grade[1]
                                                students_grades[grade[2]]["session"] = scoresheet_session
                                                students_grades[grade[2]]["semester"] = scoresheet_semester
                                                students_grades[grade[2]]["course_code"] = scoresheet_course_code
                                                students_grades[grade[2]]["attendance"] = grade[3]
                                                students_grades[grade[2]]["assignment"] = grade[4]
                                                students_grades[grade[2]]["quiz"] = grade[5]
                                                students_grades[grade[2]]["test"] = grade[6]
                                                students_grades[grade[2]]["ca_total"] = grade[7]
                                                students_grades[grade[2]]["exam_q1"] = grade[8]
                                                students_grades[grade[2]]["exam_q2"] = grade[9]
                                                students_grades[grade[2]]["exam_q3"] = grade[10]
                                                students_grades[grade[2]]["exam_q4"] = grade[11]
                                                students_grades[grade[2]]["exam_q5"] = grade[12]
                                                students_grades[grade[2]]["exam_total"] = grade[13]
                                        
                                        for student_key, student_value in students_grades.items():
                                            for grade_key, grade_value in student_value.items():
                                                if not students_grades[student_key][grade_key]:
                                                    message['outcome'] = "Failed!"
                                                    message['message'] = f"Please fill up the scoresheet! {students_grades[student_key]['name']}'s grades are not completely filled up."
                                                    message['color'] = "red"
                                        
                                        if not message["outcome"]:
                                            message['outcome'] = "Success!"
                                            message['message'] = "Scoresheet uploaded!"
                                            message['color'] = "green"

                except IndexError:
                    message['outcome'] = "Failed!"
                    message['message'] = "Please upload only the updated file of the downloaded scoresheet from STEP 1 without renaming the filename!"
                    message['color'] = "red"
            else:
                message['outcome'] = "Failed!"
                message['message'] = "That is not a CSV file. Please upload a CSV file!"
                message['color'] = "red"
        else:
            message['outcome'] = "Failed!"
            message['message'] = "Please, upload a file!"
            message['color'] = "red"

    context = {
        'course_code': course_code,
        'message': message
    }
    return render(request, "lecturer_panel/upload.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def mastersheet(request, *args, **kwargs):
    all_departments = []
    for department_obj in DEPARTMENT:
        for departments in department_obj[1]:
            all_departments.append(departments[1])
    
    context = {
        "departments": all_departments
    }
    return render(request, 'admin_panel/mastersheet.html', context)