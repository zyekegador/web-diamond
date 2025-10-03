from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    HRJobListView,
    ApplicationCreateView,
    ApplicantApplicationListView,
    JobApplicationListView,
    ApplicationDetailView,
    ApplicationStatusUpdateView,
    EducationOptionsView,
    EligibilityOptionsView,
    submit_application_simple
)

urlpatterns = [
    # Public job endpoints
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    
    # HR job management
    path('hr/jobs/', HRJobListView.as_view(), name='hr-job-list'),
    path('hr/jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('hr/jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('hr/jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    
    # Application endpoints
    path('applications/apply/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/my-applications/', ApplicantApplicationListView.as_view(), name='my-applications'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('apply-simple/', submit_application_simple, name='apply-simple'),
    
    # HR application management
    path('hr/jobs/<int:job_id>/applications/', JobApplicationListView.as_view(), name='job-applications'),
    path('hr/applications/<int:pk>/update-status/', ApplicationStatusUpdateView.as_view(), name='application-update-status'),

    path('options/education/', EducationOptionsView.as_view(), name='education-options'),
    path('options/eligibility/', EligibilityOptionsView.as_view(), name='eligibility-options'),
]