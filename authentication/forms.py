from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class AuthenticateUser(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )