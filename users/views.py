from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin # в классах представлениях вместо аннотации (проверяет авторизацию)
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm # подключаем и + там есть ссылка на модель User
    # success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index') # целевая страница
    
    def form_valid(self, form): # автоматитчески проверяет аутентификацию и потом код ниже
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # delete old authorized user carts
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user carts from anonimous session
                Cart.objects.filter(session_key=session_key).update(user=user) # подвязываем корзины

                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'

        # Можно вынести сам запрос в отдельный метод этого класса контроллера
        context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))
# оставляем функцией либо в юрелах импортируем LogoutView и направляем на него пост запрос с csfs токеном


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST) # заполняем форму инпутом пользователя (словарем)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password) # проверка наличия пользователя, возв юзера

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user) # авторизуем
#                 messages.success(request, f"{username}, Вы вошли в аккаунт") # обратная связь с пользователем

#                 if session_key:
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Cart.objects.filter(session_key=session_key).update(user=user)
                    
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next')) # перенаправление на страницу которую вблил юзер в url но для которой нужен вход в акк
                
#                 return HttpResponseRedirect(reverse('main:index')) # перенаправление, reverse() преобр в url адрес
#     else:
#         form = UserLoginForm() # пустая форма

#     context = {
#         'title': 'Home - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save() # сохранение в бд нового юзера

#             session_key = request.session.session_key

#             user = form.instance # получение пользователя из формы
#             auth.login(request, user) # обход повторного ввода логина и пароля

#             if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#             messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm() # пустая форма

#     context = {
#         'title': 'Home - Регистрация',
#         'form': form
#     }
#     return render(request, 'users/registration.html', context)


# @login_required # запрещаем доступ неавторизованным юзерам
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save() # сохранение в бд изменения юзера
#             messages.success(request, "Профиль успешно обновлен")
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user) # форма c имеющимися данными о юзере

#     orders = ( # все заказы юзера
#         Order.objects.filter(user=request.user)
#             .prefetch_related( # тк OrderItem ссылается fk на Order
#                 Prefetch(
#                     'orderitem_set', # название выборки
#                     queryset=OrderItem.objects.select_related('product'),
#                 )
#             )
#             .order_by('-id')
#         )
#     context = {
#         'title': 'Home - Кабинет',
#         'form': form,
#         'orders': orders
#     }
#     return render(request, 'users/profile.html', context)


# def users_cart(request):
#     return render(request, 'users/users_cart.html')