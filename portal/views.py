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

    context = {
        'objects': reversed(queryset),
        "students_num_count": students_num_count,
        "students_word_count": students_word_count,
        "staff_num_count": staff_num_count,
        "staff_word_count": staff_word_count,
        "course_num_count": course_num_count,
        "course_word_count": course_word_count,
    }
    return render(request, "index.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def courses(request):
    return render(request, "courses.html")

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def attendance(request):
    return render(request, "attendance.html")

@login_required(login_url='authentication')
@user_group(allowed_roles=['students', 'staff'])
def notification(request):
    return render(request, "notification.html")

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def records(request):
    return render(request, "records.html")

@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def result(request):
    return render(request, "result.html")

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

# Lecturer Panel

@login_required(login_url='authentication')
def lecturer_courses(request):
    return render(request, "lecturer_panel/courses.html")

@login_required(login_url='authentication')
def lecturer_scoresheet(request):
    return render(request, "lecturer_panel/scoresheet.html")

@login_required(login_url='authentication')
def lecturer_upload(request):
    return render(request, "lecturer_panel/upload.html")