from django.urls import path

from main import views

app_name = 'main'
# маршруты:
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    # path('about/', views.about, name='about'),
    path('delivery_payment/', views.DeliveryPaymentView.as_view(), name='delivery_payment'),
    path('contact_info/', views.ContactInfoView.as_view(), name='contact_info'),
]