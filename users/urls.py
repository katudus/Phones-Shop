from django.urls import path

from users import views

app_name = 'users' # для соед с путями сеттингс.пай

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    # path('login/', views.login, name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    # path('registration/', views.registration, name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    # path('profile/', views.profile, name='profile'),
    path('users-cart/', views.UserCartView.as_view(), name='users_cart'),
    # path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout')
]