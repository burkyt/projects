from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from conf.models import Task


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'created_date')
        exclude = ("user",)
        widgets = {
            'created_date': DateInput()
        }


class UserForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
