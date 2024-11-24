# валидация данных
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm): # описание формы

    class Meta: # с какой моделью работает эта форма
        model = User
        fields = ['username', 'password']
        
    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(
    #     label = 'Имя пользователя',
    #     widget = forms.TextInput(attrs={'autofocus': True,
    #                                     'class': 'form-control',
    #                                     'placeholder': 'Введите ваше имя пользователя'})
    # )
    # password = forms.CharField(
    #     label = 'Пароль',
    #     widget = forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                     'class': 'form-control',
    #                                     'placeholder': 'Введите ваш пароль'})
    # )
