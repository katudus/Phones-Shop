from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # заполняем форму инпутом пользователя (словарем)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # проверка наличия пользователя, возв юзера

            session_key = request.session.session_key

            if user:
                auth.login(request, user) # авторизуем
                messages.success(request, f"{username}, Вы вошли в аккаунт") # обратная связь с пользователем

                if session_key:
                    # delete old authorized user carts
                    forgot_carts = Cart.objects.filter(user=user)
                    if forgot_carts.exists():
                        forgot_carts.delete()
                    # add new authorized user carts from anonimous session
                    Cart.objects.filter(session_key=session_key).update(user=user)
                    
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
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

            session_key = request.session.session_key

            user = form.instance # получение пользователя из формы
            auth.login(request, user) # обход повторного ввода логина и пароля

            if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)
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

    orders = ( # все заказы юзера
        Order.objects.filter(user=request.user)
            .prefetch_related( # тк OrderItem ссылается fk на Order
                Prefetch(
                    'orderitem_set', # название выборки
                    queryset=OrderItem.objects.select_related('product'),
                )
            )
            .order_by('-id')
        )
    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'orders': orders
    }
    return render(request, 'users/profile.html', context)


def users_cart(request):
    return render(request, 'users/users_cart.html')


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))