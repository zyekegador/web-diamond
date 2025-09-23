from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import JobPosting, JobApplication
from .serializers import JobPostingSerializer, JobApplicationSerializer, PublicJobSerializer

# PUBLIC ENDPOINTS (No authentication required)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_job_listings(request):
    """Get all active job postings - public endpoint"""
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    serializer = PublicJobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_job_detail(request, job_id):
    """Get specific job details - public endpoint"""
    try:
        job = JobPosting.objects.get(id=job_id, is_active=True)
        serializer = PublicJobSerializer(job)
        return Response(serializer.data)
    except JobPosting.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([MultiPartParser, FormParser])
def submit_application(request):
    """Submit job application - public endpoint"""
    serializer = JobApplicationSerializer(data=request.data)
    
    if serializer.is_valid():
        application = serializer.save()
        
        # Send confirmation email (optional)
        try:
            send_mail(
                subject=f'Application Received - {application.job.title}',
                message=f'Dear {application.full_name},\n\nThank you for applying to {application.job.title}. We have received your application and will review it shortly.\n\nBest regards,\nHR Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=True,
            )
        except:
            pass  # Don't fail if email doesn't work
        
        return Response({
            'message': 'Application submitted successfully',
            'application_id': application.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PROTECTED ENDPOINTS (HR/Admin only)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_listings(request):
    """Get all job postings for HR/Admin"""
    if request.user.user_type not in ['hr', 'admin']:
        return Response({'error': 'HR or Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    jobs = JobPosting.objects.all().order_by('-created_at')
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_job(request):
    """Create new job posting - HR/Admin only"""
    if request.user.user_type not in ['hr', 'admin']:
        return Response({'error': 'HR or Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = JobPostingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_applications(request, job_id=None):
    """Get applications for specific job or all applications"""
    if request.user.user_type not in ['hr', 'admin']:
        return Response({'error': 'HR or Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    if job_id:
        applications = JobApplication.objects.filter(job_id=job_id)
    else:
        applications = JobApplication.objects.all()
    
    applications = applications.order_by('-applied_at')
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_application_status(request, application_id):
    """Update application status - HR/Admin only"""
    if request.user.user_type not in ['hr', 'admin']:
        return Response({'error': 'HR or Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        application = JobApplication.objects.get(id=application_id)
        new_status = request.data.get('status')
        
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return Response({'message': 'Status updated successfully'})
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)