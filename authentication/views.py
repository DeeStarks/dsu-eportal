from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from .forms import AuthenticateUser, CreateUser
from myapp.decorators import authenticated_user, user_group
from django.contrib.auth.models import User

# Create your views here.
@authenticated_user
def login_user(request):
    message = ''
    if request.method == 'POST':
        form = AuthenticateUser(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            message = "Username or Password incorrect"
    else:
        form = AuthenticateUser()
    context = {
        'form': form,
        'message': message
    }
    return render(request, "auth.html", context)


@user_group(allowed_roles=['admin'])
def create_user(request):
    error = {}
    success = ''
    user_object = User.objects.get(username=request.user)
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            acct_type = request.POST.get('user_group')
            group = None
            if acct_type == None:
                group = Group.objects.get(name='students')
            else:
                group = Group.objects.get(name=acct_type) 


            user.groups.add(group)
            success = f"Account created for {username} Successfully."
            user_object = User.objects.get(username=username)
            form = CreateUser()
        else:
            all__users = User.objects.all()
            if request.POST.get('username') in [user.username for user in all__users]:
                error['username'] = "Username already exist"
            elif len(form.cleaned_data.get('password1')) < 8 or form.cleaned_data.get('password1').isnumeric():
                error['password'] = "Password is not valid"
            elif form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                error['password'] = "Password did not match"
    else:
        form = CreateUser()

    context = {
        'form': form,
        'error': error,
        'success': success,
        'user_object': user_object
    }
    return render(request, "register.html", context)

def logout_user(request):
    logout(request)
    return redirect('authentication')