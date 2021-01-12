from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from myapp.decorators import user_group
from django.contrib.auth.models import User
from .models import UserProfile
from PIL import Image

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
        'success': success
    }
    return render(request, 'admin_panel/profile-edit.html', context)