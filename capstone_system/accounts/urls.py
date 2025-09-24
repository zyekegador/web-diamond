from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_hr, name='register_hr'),
    path('login/', views.login_hr, name='login_hr'),
]