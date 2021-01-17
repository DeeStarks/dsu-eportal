from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from django.contrib.auth.models import User
from .models import UserProfile, StudentCourses
from PIL import Image
from courses.models import Course

# Create your views here.

@login_required(login_url='authentication')
def profile(request, group, user_id, *args, **kwargs):
    user = User.objects.get(id=user_id)
    date = request.user.date_joined
    full_name = request.user.get_full_name()
    short_name = request.user.get_short_name()
    context = {
        "date_joined": date,
        "full_name": full_name,
        "short_name": short_name,
        "user": user
    }
    return render(request, "profile.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin',])
def update_profile(request, user_id, user_name):
    user = User.objects.get(id=user_id)
    course_set = Course.objects.all()
    user_course_object = StudentCourses.objects.filter(user=user)
    success = ''
    if request.method == 'POST':
        if user.groups.filter(name='students'):
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            reg_no = request.POST['reg_no']
            degree = request.POST['degree']
            level = request.POST['level']
            faculty = request.POST['faculty']
            department = request.POST['department']
            courses = request.POST.getlist('courses')
            if request.FILES:
                p_pic = request.FILES['p_pic']
            else:
                user_object = UserProfile.objects.get(user=user)
                p_pic = user_object.profile_pic

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()


            # Handling students courses
            student_profile = StudentCourses.objects.filter(user=user)
            student_courses = [object.courses.course_code for object in student_profile]


            core_courses = Course.objects.filter(grouping='CORE').filter(department=department)
            general_courses = Course.objects.filter(grouping="GENERAL STUDIES")

            for course in core_courses:
                if course.course_code not in student_courses:
                    StudentCourses.objects.create(
                        user=user,
                        courses=course
                    )
                
            for course in general_courses:
                if course.course_code not in student_courses:
                    StudentCourses.objects.create(
                        user=user,
                        courses=course
                    )

            if len(courses) >= 1:
                for course in courses:
                    course_object = Course.objects.get(course_code=course)
                    if course not in student_courses:
                        StudentCourses.objects.create(
                            user=user,
                            courses=course_object
                        )

            # Updating student's profile
            try:
                UserProfile.objects.create(
                    user=user,
                    profile_pic=p_pic,
                    phone=phone,
                    address=address,
                    reg_no=reg_no,
                    level=level,
                    faculty=faculty,
                    department=department,
                    degree=degree
                )
            except:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.user = user
                user_profile.phone = phone
                user_profile.profile_pic = p_pic
                user_profile.address = address
                user_profile.reg_no = reg_no
                user_profile.level = level
                user_profile.faculty = faculty
                user_profile.department = department
                user_profile.degree = degree
                user_profile.save()
            return redirect('students')

        elif user.groups.filter(name='staff'):
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            if request.FILES:
                p_pic = request.FILES['p_pic']
            else:
                user_object = UserProfile.objects.get(user=user)
                p_pic = user_object.profile_pic

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            try:
                UserProfile.objects.create(
                    user=user,
                    profile_pic=p_pic,
                    phone=phone,
                    address=address
                )
            except:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.user = user
                user_profile.phone = phone
                user_profile.profile_pic = p_pic
                user_profile.address = address
                user_profile.save()
            return redirect('staff')

        elif user.groups.filter(name='admin'):
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            if request.FILES:
                p_pic = request.FILES['p_pic']
            else:
                user_object = UserProfile.objects.get(user=user)
                p_pic = user_object.profile_pic

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            try:
                UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    profile_pic=p_pic,
                    address=address
                )
            except:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.user = user
                user_profile.phone = phone
                user_profile.profile_pic = p_pic
                user_profile.address = address
                user_profile.save()
            success = "Your account was updated!"


    context = {
        'user': user,
        'user_object': user_course_object,
        'user_course_list': [object.courses.course_code for object in user_course_object],
        'success': success,
        'elective_courses': Course.objects.filter(grouping='ELECTIVE')
    }
    return render(request, 'admin_panel/profile-edit.html', context)