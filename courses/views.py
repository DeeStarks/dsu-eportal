from django.shortcuts import render, redirect
from .models import Course, CourseAllocation
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def all_courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, "admin_panel/courses.html", context)

@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def add_course(request):
    global add_course_msg
    add_course_msg = ''
    if request.method == "POST":
        code = request.POST.get("code")
        title = request.POST.get("title")
        unit = request.POST.get("unit")
        group = None
        if request.POST.get("group") == "core":
            group = "CORE"
        elif request.POST.get("group") == "elect":
            group = "ELECTIVE"
        elif request.POST.get("group") == "gns":
            group = "GENERAL STUDIES"
        Course.objects.create(course_code=code, course_title=title, course_unit=unit, grouping=group)
        add_course_msg = 'Course Added!'

    context = {
        'success': add_course_msg
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
        'lecturer': ''
    }
    if request.method == "POST":
        lecturer = request.POST.get('lecturer')
        selected__courses = request.POST.getlist('courses')
        if lecturer:
            returned_object['lecturer'] = User.objects.get(username=lecturer)

        course_added = []
        if lecturer == None:
            returned_object['success'] = 'Failed!'
            returned_object['message'] = 'Please select a lecturer to allocate courses. '
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
                    staff_objects = CourseAllocation.objects.filter(staff_name=lecturer__selected)
                    staff_course__list = []
                    for object_item in staff_objects:
                        staff_course__list.append(object_item.course.course_code)

                    if each_course not in staff_course__list:
                        CourseAllocation.objects.create(
                            staff_name=lecturer__selected,
                            course=course__selected
                        )
                        returned_object['success'] = 'Success!'
                        returned_object['color'] = 'green'
                        returned_object['message'] = f'Course allocated for {lecturer__selected.get_full_name()}. '
                        course_added.append(each_course)
                    else:
                        returned_object['success'] = 'Success!'
                        returned_object['color'] = 'green'
                        returned_object['courses'] += f"{each_course}, "
                
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