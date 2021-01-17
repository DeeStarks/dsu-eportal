from django.shortcuts import render, redirect
from .models import Course, CourseAllocation
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from django.contrib.auth.models import User, Group
from user_profile.models import StudentCourses, UserProfile

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def all_courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses.order_by('course_code')
    }
    return render(request, "admin_panel/courses.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def add_course(request):
    global add_course_msg
    returned_object = {
        "success": '',
        "color": '',
        "message": ''
    }
    print([course.course_code for course in Course.objects.filter(grouping='CORE').filter(department='COMPUTER_SCIENCE')])
    add_course_msg = ''
    course_list = []
    for course in Course.objects.all():
        course_list.append(course.course_code)
        
    if request.method == "POST":
        code = request.POST.get("code")
        title = request.POST.get("title")
        unit = request.POST.get("unit")
        group = request.POST.get("group")
        department = request.POST.get("department")

        if code.upper() not in course_list:
            if department and group == 'CORE':
                Course.objects.create(course_code=code.upper(), course_title=title, course_unit=unit, grouping=group, department=department)

                returned_object["success"] = "Success"
                returned_object["color"] = "green"
                returned_object["message"] = "Course added!"
                
                # Add new course to related students' courses
                all_students = Group.objects.get(name='students').user_set.all()
                for student in all_students:
                    student_user_info = UserProfile.objects.get(user=student)
                    student_profile = StudentCourses.objects.filter(user=student)
                    student_courses = [object.courses.course_code for object in student_profile]


                    core_courses = Course.objects.filter(grouping='CORE').filter(department=department)
                    general_courses = Course.objects.filter(grouping="GENERAL STUDIES")

                    for course in core_courses:
                        if course.course_code not in student_courses and student_user_info.department == department:
                            StudentCourses.objects.create(
                                user=student,
                                courses=course
                            )
                        
                    for course in general_courses:
                        if course.course_code not in student_courses:
                            StudentCourses.objects.create(
                                user=student,
                                courses=course
                            )

            elif group == 'CORE' and not department:
                returned_object["success"] = "Failed!"
                returned_object["color"] = "red"
                returned_object["message"] = "You selected 'CORE' but didn't select a department!"
            else:
                Course.objects.create(course_code=code.upper(), course_title=title, course_unit=unit, grouping=group)

                returned_object["success"] = "Success"
                returned_object["color"] = "green"
                returned_object["message"] = "Course added!"
                
                # Add new course to related students' courses
                all_students = Group.objects.get(name='students').user_set.all()
                for student in all_students:
                    student_user_info = UserProfile.objects.get(user=student)
                    student_profile = StudentCourses.objects.filter(user=student)
                    student_courses = [object.courses.course_code for object in student_profile]


                    core_courses = Course.objects.filter(grouping='CORE').filter(department=department)
                    general_courses = Course.objects.filter(grouping="GENERAL STUDIES")

                    for course in core_courses:
                        if course.course_code not in student_courses and student_user_info.department == department:
                            StudentCourses.objects.create(
                                user=student,
                                courses=course
                            )
                        
                    for course in general_courses:
                        if course.course_code not in student_courses:
                            StudentCourses.objects.create(
                                user=student,
                                courses=course
                            )
        else:
            returned_object["success"] = "Failed!"
            returned_object["color"] = "red"
            returned_object["message"] = "Course already exists"


    context = {
        'info_object': returned_object
    }
    return render(request, "admin_panel/add_course.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def remove_course(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        'course': course
    }
    return render(request, "admin_panel/remove_course.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def confirm_remove(request, course_id):
    Course.objects.filter(id=course_id).delete()
    return redirect('all courses')

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def allocate_course(request):
    staff = User.objects.filter(groups__name='staff')
    courses = Course.objects.all()
    returned_object = {
        'success': '',
        'message': '',
        'courses': '',
        'color': None,
        'lecturer': '',
        'course_count': 0
    }
    if request.method == "POST":
        lecturer = request.POST.get('lecturer')
        selected__courses = request.POST.getlist('courses')
        if lecturer:
            returned_object['lecturer'] = User.objects.get(username=lecturer)

        course_added = []
        if lecturer == None:
            returned_object['success'] = 'Failed!'
            returned_object['message'] = 'Please select a lecturer to allocate course(s). '
            returned_object['color'] = 'red'
        elif len(selected__courses) == 0:
            returned_object['success'] = 'Failed!'
            returned_object['message'] = f'Please select course(s) to allocate for {User.objects.get(username=lecturer).get_full_name()}. '
            returned_object['color'] = 'red'
        else:
            for each_course in selected__courses:
                if each_course not in course_added:
                    lecturer__selected = User.objects.get(username=lecturer)
                    course__selected = Course.objects.filter(course_code=each_course)[0]
                    course_objects = CourseAllocation.objects.all()
                    course_objects__list = []
                    for course_object in course_objects:
                        course_objects__list.append(course_object.course.course_code)

                    if each_course not in course_objects__list:
                        CourseAllocation.objects.create(
                            staff_name=lecturer__selected,
                            course=course__selected
                        )
                        returned_object['success'] = 'Success!'
                        returned_object['color'] = 'green'
                        returned_object['message'] = f'Course(s) allocated to {lecturer__selected.get_full_name()}. '
                        course_added.append(each_course)
                    else:
                        returned_object['success'] = 'Success!'
                        returned_object['color'] = 'green'
                        returned_object['courses'] += f"{each_course}, "
                        returned_object['course_count'] += 1
                
    context = {
        'lecturers': staff,
        'courses': courses.order_by('course_code'),
        'returned_object': returned_object
    }
    return render(request, "admin_panel/course-allocate.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def allocated_list(request):
    message = ''
    staff_profile = User.objects.get(username=request.user.username)
    course_allocated = CourseAllocation.objects.all()

    staff_objects = []
    for staff_course in course_allocated:
        if len(staff_objects) == 0:
            staff_objects.append({
                'username': staff_course.staff_name.username,
                'fullname': staff_course.staff_name.get_full_name(),
                'courses': [staff_course.course.course_code]
            })
        elif staff_course.staff_name.username not in [staff['username'] for staff in staff_objects]:
            staff_objects.append({
                'username': staff_course.staff_name.username,
                'fullname': staff_course.staff_name.get_full_name(),
                'courses': [staff_course.course.course_code]
            })
        else:
            for staff in staff_objects:
                if staff['username'] == staff_course.staff_name.username:
                    staff['courses'].append(staff_course.course.course_code)
                    
    if request.method == 'POST':
        courses_removed = request.POST.getlist("remove_course")
        staff_name = request.POST.get('staff_name')
        staff__profile = User.objects.get(username=staff_name)

        for course in courses_removed:
            staff_courses = CourseAllocation.objects.filter(staff_name=staff__profile)
            for staff_course in staff_courses:
                if staff_course.course.course_code == course:
                    staff_course.delete()
                    message = 'Course removed successfully.'



    context = {
        'staff_objects': staff_objects,
        'message': message
    }
    return render(request, "admin_panel/allocated-list.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['staff'])
def allocated_course(request):
    staff_object = User.objects.get(username=request.user.username)
    course_allocated = CourseAllocation.objects.filter(staff_name=staff_object)
    
    context = {
        'course': course_allocated
    }
    return render(request, "lecturer_panel/courses.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['students'])
def courses(request):
    level = UserProfile.objects.get(user=request.user).level

    student_course_objects = StudentCourses.objects.filter(user=request.user)

    user_courses = []

    if level == 'FRESHMAN':
        for course in student_course_objects:
            for num in range(100, 200):
                if str(num) in course.courses.course_code:
                    user_courses.append(course)
    elif level == 'SOPHOMORE':
        for course in student_course_objects:
            for num in range(200, 300):
                if str(num) in course.courses.course_code:
                    user_courses.append(course)
    elif level == 'JUNIOR':
        for course in student_course_objects:
            for num in range(300, 400):
                if str(num) in course.courses.course_code:
                    user_courses.append(course)
    elif level == 'SENIOR':
        for course in student_course_objects:
            for num in range(400, 500):
                if str(num) in course.courses.course_code:
                    user_courses.append(course)

    total_unit = 0
    for course in user_courses:
        total_unit+=int(course.courses.course_unit)
    context = {
        'user_courses': user_courses,
        'total_unit': total_unit
    }
    return render(request, "courses.html", context)