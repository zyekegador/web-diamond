from django.urls import path
from . import views
from django.http import JsonResponse

def api_root(request):
    """API root endpoint that lists available endpoints"""
    return JsonResponse({
        'message': 'Jobs API',
        'public_endpoints': {
            'job_listings': '/api/public/jobs/',
            'job_detail': '/api/public/jobs/{id}/',
            'submit_application': '/api/public/apply/',
        },
        'protected_endpoints': {
            'manage_jobs': '/api/jobs/',
            'create_job': '/api/jobs/create/',
            'applications': '/api/applications/',
            'job_applications': '/api/jobs/{id}/applications/',
            'update_status': '/api/applications/{id}/status/',
        }
    })

urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api_root'),
    
    # Public endpoints (no auth required)
    path('public/jobs/', views.public_job_listings, name='public_job_listings'),
    path('public/jobs/<int:job_id>/', views.public_job_detail, name='public_job_detail'),
    path('public/apply/', views.submit_application, name='submit_application'),
    
    # Protected endpoints (HR/Admin only)
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('applications/', views.job_applications, name='all_applications'),
    path('jobs/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('applications/<int:application_id>/status/', views.update_application_status, name='update_application_status'),
]