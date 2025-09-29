from django.urls import path
from .views import (
    ApplicantRegisterView,
    HRCreateView,
    LoginView,
    LogoutView,
    CurrentUserView,
    HRListView
)

urlpatterns = [
    path('register/applicant/', ApplicantRegisterView.as_view(), name='applicant-register'),
    path('create/hr/', HRCreateView.as_view(), name='hr-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('hr/list/', HRListView.as_view(), name='hr-list'),
]