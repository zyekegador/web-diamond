from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Job, Application
from .models import EducationCategory, EligibilityCategory
from .serializers import (
    JobSerializer,
    JobCreateSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusUpdateSerializer,
    EducationCategorySerializer,  
    EligibilityCategorySerializer
)


class JobListView(generics.ListAPIView):
    """List all open jobs - Public access"""
    queryset = Job.objects.filter(status='open')
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]


class JobDetailView(generics.RetrieveAPIView):
    """Get single job details - Public access"""
    queryset = Job.objects.filter(status='open')
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]


class JobCreateView(generics.CreateAPIView):
    """HR can create jobs"""
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is HR
        if request.user.user_type != 'hr':
            return Response(
                {'error': 'Only HR staff can create jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(posted_by=request.user)
        
        return Response(
            JobSerializer(job).data,
            status=status.HTTP_201_CREATED
        )


class JobUpdateView(generics.UpdateAPIView):
    """HR can update their own jobs"""
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'hr':
            return Job.objects.filter(posted_by=self.request.user)
        return Job.objects.none()


class JobDeleteView(generics.DestroyAPIView):
    """HR can delete their own jobs"""
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'hr':
            return Job.objects.filter(posted_by=self.request.user)
        return Job.objects.none()


class HRJobListView(generics.ListAPIView):
    """HR can see their posted jobs"""
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'hr':
            return Job.objects.filter(posted_by=self.request.user)
        return Job.objects.none()


class ApplicationCreateView(generics.CreateAPIView):
    """Applicants can apply for jobs"""
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is applicant
        if request.user.user_type != 'applicant':
            return Response(
                {'error': 'Only applicants can apply for jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        application = serializer.save(applicant=request.user)
        
        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED
        )


class ApplicantApplicationListView(generics.ListAPIView):
    """Applicants can see their own applications"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'applicant':
            return Application.objects.filter(applicant=self.request.user)
        return Application.objects.none()


class JobApplicationListView(generics.ListAPIView):
    """HR can see applications for their jobs"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        if self.request.user.user_type == 'hr':
            return Application.objects.filter(
                job_id=job_id,
                job__posted_by=self.request.user
            )
        return Application.objects.none()


class ApplicationDetailView(generics.RetrieveAPIView):
    """View single application"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'applicant':
            return Application.objects.filter(applicant=user)
        elif user.user_type == 'hr':
            return Application.objects.filter(job__posted_by=user)
        return Application.objects.none()


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    """HR can update application status"""
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'hr':
            return Application.objects.filter(job__posted_by=self.request.user)
        return Application.objects.none()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(ApplicationSerializer(instance).data)

class EducationOptionsView(APIView):
    """Returns all education options grouped by category"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = EducationCategory.objects.filter(is_active=True).prefetch_related('programs')
        serializer = EducationCategorySerializer(categories, many=True)
        return Response(serializer.data)


class EligibilityOptionsView(APIView):
    """Returns all eligibility options grouped by category"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = EligibilityCategory.objects.filter(is_active=True).prefetch_related('types')
        serializer = EligibilityCategorySerializer(categories, many=True)
        return Response(serializer.data)