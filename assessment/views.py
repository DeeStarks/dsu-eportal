from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myapp.decorators import user_group
from courses.models import CourseAllocation
import os
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
def scoresheet_upload(request, course):
    context = {
        'course': course
    }
    return render(request, "lecturer_panel/upload.html", context)
    
@login_required(login_url='authentication')
@user_group(allowed_roles=['admin'])
def mastersheet(request, *args, **kwargs):
    context = {

    }
    return render(request, 'admin_panel/mastersheet.html', context)