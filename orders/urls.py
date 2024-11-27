from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    # path('create-order/', views.create_order, name='create_order'),
]
