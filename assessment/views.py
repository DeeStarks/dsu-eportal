from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myapp.decorators import user_group
from courses.models import CourseAllocation
import io
from django.template.loader import get_template, render_to_string
# import weasyprint
from xhtml2pdf import pisa
import os
from pathlib import Path
import csv
from session_semester.models import SessionAndSemester
from user_profile.models import StudentCourses, UserProfile, DEPARTMENT
from courses.models import Course
from .models import ContinousAssessment, StudentGrade, UploadedScoresheets, CarryOver, ReleaseResult
from django.core.exceptions import ObjectDoesNotExist

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
            [f"Lecturer's Name: {request.user.get_full_name()}"]
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
        renamed_sheet = None
        if request.FILES:
            sheet = request.FILES.get('sheet')
            for i in range(1000):
                if sheet.name.split('.')[0].endswith(f" ({i})"):
                    renamed_sheet = sheet.name.replace(f" ({i})", '')
            if renamed_sheet:
                sheet.name = renamed_sheet

        if sheet != None:
            if sheet.name.endswith(".csv"):
                available_sheets = [sheet.sheet_name for sheet in UploadedScoresheets.objects.all()]
                if renamed_sheet in available_sheets:
                    message['outcome'] = "Failed!"
                    message['message'] = "Oops! The scoresheet you uploaded already exists and it can no longer be updated. If you need to make changes, contact an Admin!"
                    message['color'] = "red"
                else:
                    try:
                        sheet_name = sheet.name.split("-")
                        scoresheet_session = sheet_name[0].replace("_", "/")
                        scoresheet_semester = sheet_name[1]
                        scoresheet_course_code = sheet_name[2]
                        session__semester = SessionAndSemester.objects.get(id=1)
                        if scoresheet_course_code != course_code:
                            message['outcome'] = "Failed!"
                            message['message'] = f"You uploaded a scoresheet with course code - {scoresheet_course_code}, instead of {course_code}"
                            message['color'] = "red"
                        elif scoresheet_session != session__semester.session:
                            message['outcome'] = "Failed!"
                            message['message'] = f"You uploaded a scoresheet with another session."
                            message['color'] = "red"
                        elif scoresheet_semester != session__semester.semester:
                            message['outcome'] = "Failed!"
                            message['message'] = f"You uploaded a scoresheet with another semester."
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
                                                    students_grades[grade[2]]["session"] = scoresheet_session
                                                    students_grades[grade[2]]["semester"] = scoresheet_semester
                                            
                                            for student_key, student_value in students_grades.items():
                                                for grade_key, grade_value in student_value.items():
                                                    if students_grades[student_key][grade_key] == '':
                                                        message['outcome'] = "Failed!"
                                                        message['message'] = f"Oops! The scoresheet is not filled completely. Please fill up the scoresheet!."
                                                        message['color'] = "red"
                                            
                                            if not message['outcome']:
                                                for student_key, student_value in students_grades.items():
                                                    for grade_key, grade_value in student_value.items():
                                                        if not students_grades[student_key]["ca_total"].isnumeric():
                                                            message['outcome'] = "Failed!"
                                                            message['message'] = f"Please the grades should be recorded numerically! {students_grades[student_key]['name']}'s Continous Assessment Total Score is not a number."
                                                            message['color'] = "red"
                                                            
                                            if not message['outcome']:
                                                for student_key, student_value in students_grades.items():
                                                    for grade_key, grade_value in student_value.items():
                                                        if not students_grades[student_key]["exam_total"].isnumeric():
                                                            message['outcome'] = "Failed!"
                                                            message['message'] = f"Please the grades should be recorded numerically! {students_grades[student_key]['name']}'s Examination Total Score is not a number."
                                                            message['color'] = "red"

                                            
                                            if not message["outcome"]:
                                                # Creating the continous assessment for the semester
                                                for student_object in students_grades:
                                                    student = User.objects.get(username=student_object)
                                                    course = Course.objects.get(course_code=students_grades[student_object]['course_code'])
                                                    ca_total = int(students_grades[student_object]['ca_total'])
                                                    exam_total = int(students_grades[student_object]['exam_total'])
                                                    total = ca_total+exam_total
                                                    gp = 0
                                                    carry_over = False
                                                    if total in range(0, 40):
                                                        gp = 0
                                                        carry_over = True
                                                    elif total in range(40, 45):
                                                        gp = 1
                                                    elif total in range(45, 50):
                                                        gp = 2
                                                    elif total in range(50, 60):
                                                        gp = 3
                                                    elif total in range(60, 70):
                                                        gp = 4
                                                    elif total in range(70, 101):
                                                        gp = 5
                                                    
                                                    qp = gp*int(course.course_unit)

                                                    if students_grades[student_object]['semester'] == "First Semester":
                                                        for object in ContinousAssessment.objects.filter(semester='Second Semester'):
                                                            object.delete()
                                                    elif students_grades[student_object]['semester'] == "Second Semester":
                                                        for object in ContinousAssessment.objects.filter(semester='First Semester'):
                                                            object.delete()

                                                    ContinousAssessment.objects.create(
                                                        user=student,
                                                        course=course,
                                                        ca_total=ca_total,
                                                        exam_total=exam_total,
                                                        total=total,
                                                        grading_point=gp,
                                                        quality_point=qp,
                                                        semester=students_grades[student_object]['semester'],
                                                        session=students_grades[student_object]['session'],
                                                        level=UserProfile.objects.get(user=student).get_level_display(),
                                                        carryover=carry_over
                                                    )

                                                    if carry_over:
                                                        CarryOver.objects.create(
                                                            user=student,
                                                            course=course
                                                        )
                                                
                                                # Grading the students based on the information from the ContinousAssessment model class
                                                for student_object in students_grades:
                                                    user = User.objects.get(username=student_object)
                                                    student_ca = ContinousAssessment.objects.filter(user=user)
                                                    student_courses = StudentCourses.objects.filter(user=user)
                                                    level = UserProfile.objects.get(user=user).level

                                                    total_course_unit = 0
                                                    for course in student_courses:
                                                        if level == "FRESHMAN":
                                                            for num in range(100, 200):
                                                                if str(num) in course.courses.course_code:
                                                                    total_course_unit += int(course.courses.course_unit)
                                                        elif level == "SOPHOMORE":
                                                            for num in range(200, 300):
                                                                if str(num) in course.courses.course_code:
                                                                    total_course_unit += int(course.courses.course_unit)
                                                        elif level == "JUNIOR":
                                                            for num in range(300, 400):
                                                                if str(num) in course.courses.course_code:
                                                                    total_course_unit += int(course.courses.course_unit)
                                                        elif level == "SENIOR":
                                                            for num in range(400, 500):
                                                                if str(num) in course.courses.course_code:
                                                                    total_course_unit += int(course.courses.course_unit)

                                                    quality_point = 0
                                                    for grade in student_ca:
                                                        quality_point += grade.quality_point
                                                    gpa = None
                                                    if total_course_unit != 0:
                                                        gpa = round((quality_point/total_course_unit), 1)

                                                    attendance = int(students_grades[student_object]['attendance'])
                                                    level = UserProfile.objects.get(user=user).level
                                                    
                                                    StudentGrade.objects.update_or_create(
                                                        user=user,
                                                        session=students_grades[student_object]['session'],
                                                        semester=students_grades[student_object]['semester'],
                                                        attendance=attendance,
                                                        tcu=total_course_unit,
                                                        gpa=gpa,
                                                        level=level,
                                                        defaults={
                                                            'user': user,
                                                            'level': level,
                                                            'semester': students_grades[student_object]['semester']
                                                        }
                                                    )

                                                    # Deleting the previous user's grade manually because the StudentGrade.objects.update_or_create above isn't updating the user's grade
                                                    if StudentGrade.objects.filter(user=user).filter(level=level).filter(semester=students_grades[student_object]['semester']).count() > 1:
                                                        StudentGrade.objects.filter(user=user).filter(level=level).filter(semester=students_grades[student_object]['semester'])[0].delete()
                                                    
                                                    # Calculating cgpa
                                                    total_gradings = []
                                                    for point in StudentGrade.objects.filter(user=user):
                                                        total_gradings.append(float(point.gpa))
                                                    
                                                    # Calculating total attendance
                                                    total_attendance = []
                                                    for grade_attendance in StudentGrade.objects.filter(user=user):
                                                        total_attendance.append(int(grade_attendance.attendance))
                                                    
                                                    max_attendance = len(total_attendance)*5
                                                    student_attendance = (attendance/5)*100
                                                    if max_attendance:
                                                        student_attendance = (sum(total_attendance)/max_attendance)*100
                                                    
                                                    # Adding the CGPA and Attendance to students grades
                                                    cgpa = round((sum(total_gradings)/len(total_gradings)), 2)
                                                    print(total_gradings)
                                                    student_grade_object = StudentGrade.objects.filter(user=user).filter(level=level).get(semester=students_grades[student_object]['semester'])
                                                    student_grade_object.cgpa = cgpa
                                                    student_grade_object.attendance = student_attendance
                                                    student_grade_object.save()

                                                message['outcome'] = "Success!"
                                                message['message'] = "Scoresheet uploaded!"
                                                message['color'] = "green"
                                                
                                                # Save the uploaded filename
                                                UploadedScoresheets.objects.create(sheet_name=sheet.name)

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
    
    if request.method == "POST":
        release = request.POST.get("release_result")
        release_queryset = ReleaseResult.objects.all()
        if release == "True":
            if release_queryset.exists():
                release_object = release_queryset[0]
                release_object.release_result = True
                release_object.save()
            else:
                ReleaseResult.objects.create(
                    release_result=True
                )
        elif release == "False":
            if release_queryset.exists():
                release_object = release_queryset[0]
                release_object.release_result = False
                release_object.save()
            else:
                ReleaseResult.objects.create(
                    release_result=False
                )

    release_result = False
    if ReleaseResult.objects.all().exists():
        release_result = ReleaseResult.objects.all()[0].release_result

    
    context = {
        "departments": all_departments,
        "release_result": release_result
    }
    return render(request, 'admin_panel/mastersheet.html', context)
    
def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    else:
        return None

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def mastersheet_template(request, department, level, *args, **kwargs):
    results = {}
    semester = ContinousAssessment.objects.all()[0].semester
    session = ContinousAssessment.objects.all()[0].session
    department_reverse = dict((j, [i, k]) for k, v in DEPARTMENT for i, j in v) 
    faculty = department_reverse[department][1]
    dpt_students = UserProfile.objects.filter(department=department_reverse[department][0]).filter(level=level)
    courses_of_students = []

    for student_profile in dpt_students:
        student_courses = StudentCourses.objects.filter(user=student_profile.user)
        for course in student_courses:
            if level == "FRESHMAN":
                for num in range(100, 200):
                    if str(num) in course.courses.course_code and course.courses.course_code not in courses_of_students:
                        courses_of_students.append(Course.objects.get(course_code=course.courses.course_code))
            elif level == "SOPHOMORE":
                for num in range(200, 300):
                    if str(num) in course.courses.course_code and course.courses.course_code not in courses_of_students:
                        courses_of_students.append(Course.objects.get(course_code=course.courses.course_code))
            elif level == "JUNIOR":
                for num in range(300, 400):
                    if str(num) in course.courses.course_code and course.courses.course_code not in courses_of_students:
                        courses_of_students.append(Course.objects.get(course_code=course.courses.course_code))
            elif level == "SENIOR":
                for num in range(400, 500):
                    if str(num) in course.courses.course_code and course.courses.course_code not in courses_of_students:
                        courses_of_students.append(Course.objects.get(course_code=course.courses.course_code))
    
    for student in dpt_students:
        try:
            grades = StudentGrade.objects.filter(user=student.user).filter(level=level).get(semester=semester)

            results[student.user.username] = {
                'name': student.user.get_full_name(),
                'matric_no': student.user.username,
                'total_course_unit': grades.tcu,
                'grade_point_average': grades.gpa,
                'cumm_grade_point_average': grades.cgpa,
                'grades': []
            }

            for course in courses_of_students:
                grading_course = Course.objects.get(course_code=course.course_code)
                try:
                    course_obj = ContinousAssessment.objects.filter(user=student.user).get(course=grading_course)
                    results[student.user.username]['grades'].append(course_obj.total)
                except ObjectDoesNotExist:
                    results[student.user.username]['grades'].append('--')
        except ObjectDoesNotExist:
            results[student.user.username] = {
                'name': student.user.get_full_name(),
                'matric_no': student.user.username,
                'total_course_unit': '--',
                'grade_point_average': '--',
                'cumm_grade_point_average': '--',
                'grades': []
            }
            for course in courses_of_students:
                results[student.user.username]['grades'].append('--')
    
    context = {
        'faculty': faculty,
        'department': department,
        'session': session,
        'semester': semester,
        'courses': courses_of_students,
        'results': results
    }

    # html = render_to_string('admin_panel/mastersheet_template.htm', context)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{faculty} {department} {level} level mastersheet.pdf"'
    # weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/style.css')])
    # return response

    # pdf = render_to_pdf('admin_panel/mastersheet_template.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'admin_panel/mastersheet_template.html', context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def records(request):
    student = User.objects.get(username=request.user.username)
    grade_object = StudentGrade.objects.filter(user=student)
    grades = {
        'FRESHMAN':{
            'first_semester_gpa': '',
            'second_semester_gpa': '',
            'cgpa': ''
        },
        'SOPHOMORE':{
            'first_semester_gpa': '',
            'second_semester_gpa': '',
            'cgpa': ''
        },
        'JUNIOR':{
            'first_semester_gpa': '',
            'second_semester_gpa': '',
            'cgpa': ''
        },
        'SENIOR':{
            'first_semester_gpa': '',
            'second_semester_gpa': '',
            'cgpa': ''
        }
    }
    # Getting the student's FRESHMAN grades if exists
    try:
        grades['FRESHMAN']['first_semester_gpa'] = grade_object.filter(level="FRESHMAN").get(semester="First Semester").gpa
        grades['FRESHMAN']['cgpa'] = grade_object.filter(level="FRESHMAN").get(semester="First Semester").cgpa
    except ObjectDoesNotExist:
        grades['FRESHMAN']['first_semester_gpa'] = '--'
        grades['FRESHMAN']['cgpa'] = '--'
        
    try:
        grades['FRESHMAN']['second_semester_gpa'] = grade_object.filter(level="FRESHMAN").get(semester="Second Semester").gpa
        grades['FRESHMAN']['cgpa'] = grade_object.filter(level="FRESHMAN").get(semester="Second Semester").cgpa
    except ObjectDoesNotExist:
        grades['FRESHMAN']['second_semester_gpa'] = '--'
        grades['FRESHMAN']['cgpa'] = '--'
        
    # Getting the student's SOPHOMORE grades if exists
    try:
        grades['SOPHOMORE']['first_semester_gpa'] = grade_object.filter(level="SOPHOMORE").get(semester="First Semester").gpa
        grades['SOPHOMORE']['cgpa'] = grade_object.filter(level="SOPHOMORE").get(semester="First Semester").cgpa
    except ObjectDoesNotExist:
        grades['SOPHOMORE']['first_semester_gpa'] = '--'
        grades['SOPHOMORE']['cgpa'] = '--'
        
    try:
        grades['SOPHOMORE']['second_semester_gpa'] = grade_object.filter(level="SOPHOMORE").get(semester="Second Semester").gpa
        grades['SOPHOMORE']['cgpa'] = grade_object.filter(level="SOPHOMORE").get(semester="Second Semester").cgpa
    except ObjectDoesNotExist:
        grades['SOPHOMORE']['second_semester_gpa'] = '--'
        grades['SOPHOMORE']['cgpa'] = '--'
        
    # Getting the student's JUNIOR grades if exists
    try:
        grades['JUNIOR']['first_semester_gpa'] = grade_object.filter(level="JUNIOR").get(semester="First Semester").gpa
        grades['JUNIOR']['cgpa'] = grade_object.filter(level="JUNIOR").get(semester="First Semester").cgpa
    except ObjectDoesNotExist:
        grades['JUNIOR']['first_semester_gpa'] = '--'
        grades['JUNIOR']['cgpa'] = '--'
        
    try:
        grades['JUNIOR']['second_semester_gpa'] = grade_object.filter(level="JUNIOR").get(semester="Second Semester").gpa
        grades['JUNIOR']['cgpa'] = grade_object.filter(level="JUNIOR").get(semester="Second Semester").cgpa
    except ObjectDoesNotExist:
        grades['JUNIOR']['second_semester_gpa'] = '--'
        grades['JUNIOR']['cgpa'] = '--'
        
    # Getting the student's SENIOR grades if exists
    try:
        grades['SENIOR']['first_semester_gpa'] = grade_object.filter(level="SENIOR").get(semester="First Semester").gpa
        grades['SENIOR']['cgpa'] = grade_object.filter(level="SENIOR").get(semester="First Semester").cgpa
    except ObjectDoesNotExist:
        grades['SENIOR']['first_semester_gpa'] = '--'
        grades['SENIOR']['cgpa'] = '--'
        
    try:
        grades['SENIOR']['second_semester_gpa'] = grade_object.filter(level="SENIOR").get(semester="Second Semester").gpa
        grades['SENIOR']['cgpa'] = grade_object.filter(level="SENIOR").get(semester="Second Semester").cgpa
    except ObjectDoesNotExist:
        grades['SENIOR']['second_semester_gpa'] = '--'
        grades['SENIOR']['cgpa'] = '--'

    context = {
        'grades': grades
    }
    return render(request, "records.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def result(request):
    result = {}
    student = User.objects.get(username=request.user)
    level = UserProfile.objects.get(user=student).level
    courses_registered = []
    all_courses_registered = StudentCourses.objects.filter(user=student).order_by('courses__course_code')
    release_result = False
    release_queryset = ReleaseResult.objects.all()
    if release_queryset.exists():
        release_result = release_queryset[0].release_result

    if level == "FRESHMAN":
        for course in all_courses_registered:
            for num in range(100, 200):
                if str(num) in course.courses.course_code:
                    courses_registered.append(course)
    elif level == "SOPHOMORE":
        for course in all_courses_registered:
            for num in range(200, 300):
                if str(num) in course.courses.course_code:
                    courses_registered.append(course)
    elif level == "JUNIOR":
        for course in all_courses_registered:
            for num in range(300, 400):
                if str(num) in course.courses.course_code:
                    courses_registered.append(course)
    elif level == "SENIOR":
        for course in all_courses_registered:
            for num in range(400, 500):
                if str(num) in course.courses.course_code:
                    courses_registered.append(course)

    grades = {}
    for course in courses_registered:
        try:
            continous_assessment = ContinousAssessment.objects.filter(user=student).get(course=course.courses)
            result[course.courses.course_code] = {
                'course_code': course.courses.course_code,
                'course_title': course.courses.course_title,
                'course_unit': course.courses.course_unit,
                'continous_assessment': continous_assessment.ca_total,
                'exam_score': continous_assessment.exam_total,
                'total_score': continous_assessment.total
            }
            if continous_assessment.total in range(0, 40):
                result[course.courses.course_code]['grade_letter'] = "F"
            elif continous_assessment.total in range(40, 45):
                result[course.courses.course_code]['grade_letter'] = "E"
            elif continous_assessment.total in range(45, 50):
                result[course.courses.course_code]['grade_letter'] = "D"
            elif continous_assessment.total in range(50, 60):
                result[course.courses.course_code]['grade_letter'] = "C"
            elif continous_assessment.total in range(60, 70):
                result[course.courses.course_code]['grade_letter'] = "B"
            elif continous_assessment.total in range(70, 101):
                result[course.courses.course_code]['grade_letter'] = "A"

            grade_object = None
            if continous_assessment.level == "Freshman (100)":
                grade_object = StudentGrade.objects.filter(user=student).filter(level="FRESHMAN")
            elif continous_assessment.level == "Sophomore (200)":
                grade_object = StudentGrade.objects.filter(user=student).filter(level="SOPHOMORE")
            elif continous_assessment.level == "Junior (300)":
                grade_object = StudentGrade.objects.filter(user=student).filter(level="JUNIOR")
            elif continous_assessment.level == "Senior (400)":
                grade_object = StudentGrade.objects.filter(user=student).filter(level="SENIOR")

            grades["level"] = continous_assessment.level
            grades["semester"] = continous_assessment.semester
            try:
                grades["first_semester"] = grade_object.get(semester='First Semester').gpa
                grades['cgpa'] = grade_object.get(semester="First Semester").cgpa
            except ObjectDoesNotExist:
                grades['first_semester'] = '--'
                grades['cgpa'] = '--'
                
            try:
                grades["second_semester"] = grade_object.get(semester='Second Semester').gpa
                grades['cgpa'] = grade_object.get(semester="Second Semester").cgpa
            except ObjectDoesNotExist:
                grades['second_semester'] = '--'
                grades['cgpa'] = '--'

        except ObjectDoesNotExist:
            result[course.courses.course_code] = {
                'course_code': course.courses.course_code,
                'course_title': course.courses.course_title,
                'course_unit': course.courses.course_unit,
                'continous_assessment': "--",
                'exam_score': "--",
                'total_score': "--",
                'grade_letter': "--"
            }
    
    
    context = {
        'result_object': result,
        'grades': grades,
        'carry_over': CarryOver.objects.filter(user=student),
        'release_result': release_result
    }
    return render(request, "result.html", context)