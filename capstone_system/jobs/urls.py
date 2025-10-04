from django.urls import path
from .views import (
    # Job views
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    HRJobListView,
    
    # Application views
    ApplicationCreateView,
    ApplicantApplicationListView,
    JobApplicationListView,
    ApplicationDetailView,
    ApplicationStatusUpdateView,
    
    # Document views
    submit_complete_application,
    upload_application_document,
    get_application_documents,
    delete_application_document,
    
    # Options views
    EducationOptionsView,
    EligibilityOptionsView,
)

urlpatterns = [
    # ============= PUBLIC JOB ENDPOINTS =============
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    
    # ============= HR JOB MANAGEMENT =============
    path('hr/jobs/', HRJobListView.as_view(), name='hr-job-list'),
    path('hr/jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('hr/jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('hr/jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    
    # ============= APPLICATION SUBMISSION =============
    # Method 1: Two-step process (create application, then upload documents)
    path('applications/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:application_id>/upload-document/', upload_application_document, name='upload-document'),
    
    # Method 2: One-step process (submit everything at once) - RECOMMENDED
    path('applications/submit-complete/', submit_complete_application, name='submit-complete-application'),
    
    # ============= APPLICANT APPLICATION MANAGEMENT =============
    path('applications/my-applications/', ApplicantApplicationListView.as_view(), name='my-applications'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:application_id>/documents/', get_application_documents, name='application-documents'),
    path('documents/<int:document_id>/delete/', delete_application_document, name='delete-document'),
    
    # ============= HR APPLICATION MANAGEMENT =============
    path('hr/jobs/<int:job_id>/applications/', JobApplicationListView.as_view(), name='job-applications'),
    path('hr/applications/<int:pk>/update-status/', ApplicationStatusUpdateView.as_view(), name='application-update-status'),
    
    # ============= OPTIONS/DROPDOWN DATA =============
    path('options/education/', EducationOptionsView.as_view(), name='education-options'),
    path('options/eligibility/', EligibilityOptionsView.as_view(), name='eligibility-options'),
]