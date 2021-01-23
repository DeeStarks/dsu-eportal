from django.shortcuts import render, redirect
from django.http import HttpResponse
from post_creation.models import Post
from django.contrib.auth.decorators import login_required
import timeago, datetime
from django.contrib.auth.models import Group
from courses.models import Course
from num2words import num2words
from django.contrib.auth.models import User
from myapp.decorators import user_group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from user_profile.models import UserProfile
from assessment.models import ContinousAssessment, CarryOver
from user_profile.models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
import os
from pathlib import Path
import json
import csv

@login_required(login_url='authentication')
def index(request):
    queryset = Post.objects.all()
    staff = Group.objects.get(name='staff')
    students = Group.objects.get(name='students')
    courses = Course.objects.all()
    students_num_count = len(students.user_set.all())
    students_word_count = num2words(students_num_count)
    staff_num_count = len(staff.user_set.all())
    staff_word_count = num2words(staff_num_count)
    course_num_count = len(courses)
    course_word_count = num2words(course_num_count)
    carryover_students = []
    for student in CarryOver.objects.all():
        if student.user not in carryover_students:
            carryover_students.append(student)
    carry_overs = num2words(len(carryover_students))

    # Getting students' performance from the backend and sending to json for display on admin dashboard
    assessment = ContinousAssessment.objects.all()
    freshman_students = []
    sophomore_students = []
    junior_students = []
    senior_students = []

    for ca in assessment:
        student = ca.user
        student_profile = UserProfile.objects.get(user=student)
        student_level = student_profile.level
        if student_level == "FRESHMAN":
            freshman_students.append(ca)
        elif student_level == "SOPHOMORE":
            sophomore_students.append(ca)
        elif student_level == "JUNIOR":
            junior_students.append(ca)
        elif student_level == "SENIOR":
            senior_students.append(ca)

    freshman_performance, sophomore_performance, junior_performance, senior_performance = 0, 0, 0, 0
    freshman_total, sophomore_total, junior_total, senior_total = len(freshman_students)*100, len(sophomore_students)*100, len(junior_students)*100, len(senior_students)*100

    if freshman_students:
        for student in freshman_students:
            freshman_performance+= int(student.total)
    if sophomore_students:
        for student in sophomore_students:
            sophomore_performance+= int(student.total)
    if junior_students:
        for student in junior_students:
            junior_performance+= int(student.total)
    if senior_students:
        for student in senior_students:
            senior_performance+= int(student.total)

    freshman_percentage, sophomore_percentage, junior_percentage, senior_percentage = 0, 0, 0, 0

    if freshman_students:
        freshman_percentage = int(round(freshman_performance/freshman_total*100))
    if sophomore_students:
        sophomore_percentage = int(round(sophomore_performance/sophomore_total*100))
    if junior_students:
        junior_percentage = int(round(junior_performance/junior_total*100))
    if senior_students:
        senior_percentage = int(round(senior_performance/senior_total*100))
        
    students_total_performance = freshman_percentage + sophomore_percentage + junior_percentage + senior_percentage

    if students_total_performance == 0:
        students_total_performance = 1

    freshman_rate, sophomore_rate, junior_rate, senior_rate = freshman_percentage/10, sophomore_percentage/10, junior_percentage/10, senior_percentage/10
    
    if freshman_rate == 0 and sophomore_rate == 0 and junior_rate == 0 and senior_rate == 0:
        freshman_percentage, sophomore_percentage, junior_percentage, senior_percentage = 50, 50, 50, 50

    file_to_json = {
        "freshman_percentage": int(round((freshman_percentage/students_total_performance)*100)),
        "sophomore_percentage": int(round((sophomore_percentage/students_total_performance)*100)),
        "junior_percentage": int(round((junior_percentage/students_total_performance)*100)),
        "senior_percentage": int(round((senior_percentage/students_total_performance)*100)),
        "freshman_rate": freshman_rate,
        "sophomore_rate": sophomore_rate,
        "junior_rate": junior_rate,
        "senior_rate": senior_rate,
    }

    BASE_DIR = Path(__file__).resolve().parent.parent
    json_loc = os.path.join(BASE_DIR, 'static/admin_chart.json')
    with open(json_loc, 'w') as json_file:
        json_file.write(json.dumps(file_to_json))

    context = {
        'objects': reversed(queryset),
        "students_num_count": students_num_count,
        "students_word_count": students_word_count,
        "staff_num_count": staff_num_count,
        "staff_word_count": staff_word_count,
        "course_num_count": course_num_count,
        "course_word_count": course_word_count,
        "carryover_num_count": len(carryover_students),
        "carryover_word_count": carry_overs
    }
    return render(request, "index.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['students', 'staff', 'admin'])
def change_password(request):
    message = {
        'outcome': '',
        'message': '',
        'color': ''
    }
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        password01 = request.POST.get('password01')
        password02 = request.POST.get('password02')
        print(password01)

        if user.check_password(current_password):
            if password01 == '' or password02 == '':
                message['outcome'] = "Failed!"
                message['message'] = "Please enter new password and confirm."
                message['color'] = "red"
            else:
                if password01 != password02:
                    message['outcome'] = "Failed!"
                    message['message'] = "Oops! The new password did not match. Please re-type your new password and confirm."
                    message['color'] = "red"
                else:
                    user.password = make_password(password01)
                    user.save()
                    update_session_auth_hash(request, user)
                    message['outcome'] = "Success!"
                    message['message'] = "Your password has been changed."
                    message['color'] = "green"
        else:
            message['outcome'] = "Failed!"
            message['message'] = "Oops! The current password you entered isn't your current password. Please re-type password."
            message['color'] = "red"

    context = {
        'message': message
    }
    return render(request, 'password_change.html', context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def attendance(request):
    return render(request, "attendance.html")

@login_required(login_url='authentication')
def get_started(request):
    return render(request, "start.html")

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def voucher(request):
    return render(request, "voucher.html")

def page404(request, url):
    return render(request, "404.html")

# Admin panel
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def students(request):
    students = User.objects.filter(groups__name='students')
        
    context = {
        'students': students.order_by('first_name')
    }
    return render(request, "admin_panel/student.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def staff(request):
    staff = User.objects.filter(groups__name='staff')
    context = {
        'staff': staff.order_by('first_name')
    }
    return render(request, "admin_panel/staff.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def confirm_user_delete(request, group, username):
    queryset = User.objects.get(username=username)
    context = {
        'object': queryset
    }
    return render(request, "admin_panel/delete_user.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])  
def delete_user(request, group, username):
    user = User.objects.get(username=username)
    if user.groups.filter(name='staff'):
        User.objects.get(username=username).delete()
        return redirect('staff')
    elif user.groups.filter(name='students'):
        User.objects.get(username=username).delete()
        return redirect('students')

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])  
def redirect_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.groups.filter(name='staff'):
        return redirect('staff')
    elif user.groups.filter(name='students'):
        return redirect('students')

