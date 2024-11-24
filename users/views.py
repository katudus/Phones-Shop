from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # заполняем форму инпутом пользователя (словарем)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # проверка наличия пользователя, возв юзера
            if user:
                auth.login(request, user) # авторизуем
                return HttpResponseRedirect(reverse('main:index')) # перенаправление, reverse() преобр в url адрес
    else:
        form = UserLoginForm() # пустая форма

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save() # сохранение в бд нового юзера
            user = form.instance # получение пользователя из формы
            auth.login(request, user) # обход повторного ввода логина и пароля
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm() # пустая форма

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'Home - Кабинет'
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))