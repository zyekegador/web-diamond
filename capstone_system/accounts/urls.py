from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/pending-hr/', views.pending_hr_approvals, name='pending_hr_approvals'),
    path('admin/approve-hr/<int:user_id>/', views.approve_hr, name='approve_hr'),
]