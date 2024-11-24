from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # заполняем форму инпутом пользователя (словарем)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # проверка наличия пользователя, возв юзера
            if user:
                auth.login(request, user) # авторизуем
                messages.success(request, f"{username}, Вы вошли в аккаунт") # обратная связь с пользователем

                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next')) # перенаправление на страницу которую вблил юзер в url но для которой нужен вход в акк
                
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
            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm() # пустая форма

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required # запрещаем доступ неавторизованным юзерам
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save() # сохранение в бд изменения юзера
            messages.success(request, "Профиль успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user) # форма c имеющимися данными о юзере

    context = {
        'title': 'Home - Кабинет',
        'form': form
    }
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))