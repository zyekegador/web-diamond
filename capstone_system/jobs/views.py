from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.db import transaction

from .models import Job, Application, ApplicationDocument
from .models import EducationCategory, EligibilityCategory
from .serializers import (
    JobSerializer,
    JobCreateSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationWithDocumentsSerializer,
    ApplicationStatusUpdateSerializer,
    ApplicationDocumentSerializer,
    ApplicationDocumentCreateSerializer,
    EducationCategorySerializer,
    EligibilityCategorySerializer
)


# ============= JOB VIEWS =============

class JobListView(generics.ListAPIView):
    """List all open jobs - Public access"""
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Job.objects.filter(status='open').select_related('posted_by').prefetch_related(
            'education_levels__category',
            'eligibility_types__category'
        )


class JobDetailView(generics.RetrieveAPIView):
    """Get single job details - Public access"""
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Job.objects.filter(status='open').select_related('posted_by').prefetch_related(
            'education_levels__category',
            'eligibility_types__category'
        )


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
            return Job.objects.filter(posted_by=self.request.user).select_related('posted_by').prefetch_related(
                'education_levels__category',
                'eligibility_types__category'
            )
        return Job.objects.none()


# ============= APPLICATION VIEWS =============

class ApplicationCreateView(generics.CreateAPIView):
    """Create application without documents (Step 1)"""
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def submit_complete_application(request):
    """
    Submit complete application with all documents in one request
    Matches CSC Job Portal requirements
    """
    if request.user.user_type != 'applicant':
        return Response(
            {'error': 'Only applicants can submit applications'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = ApplicationWithDocumentsSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        try:
            with transaction.atomic():
                application = serializer.save()
                
                # Trigger OCR processing for required documents
                # (This would be handled by a background task in production)
                documents_to_process = application.documents.filter(
                    document_type__in=['pds', 'wes', 'eligibility_license', 'transcript']
                )
                
                return Response({
                    'success': True,
                    'message': 'Application submitted successfully',
                    'application': ApplicationSerializer(application).data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_application_document(request, application_id):
    """
    Upload individual document to existing application (Step 2 - document upload)
    Allows applicants to upload documents one by one
    """
    if request.user.user_type != 'applicant':
        return Response(
            {'error': 'Only applicants can upload documents'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        application = Application.objects.get(
            id=application_id,
            applicant=request.user
        )
    except Application.DoesNotExist:
        return Response(
            {'error': 'Application not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ApplicationDocumentCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        document = serializer.save(application=application)
        
        # Trigger OCR if applicable
        if document.requires_ocr:
            # Queue OCR processing task here
            pass
        
        return Response(
            ApplicationDocumentSerializer(document, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_application_documents(request, application_id):
    """Get all documents for an application"""
    try:
        if request.user.user_type == 'applicant':
            application = Application.objects.get(
                id=application_id,
                applicant=request.user
            )
        elif request.user.user_type == 'hr':
            application = Application.objects.get(
                id=application_id,
                job__posted_by=request.user
            )
        else:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_403_FORBIDDEN
            )
    except Application.DoesNotExist:
        return Response(
            {'error': 'Application not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    documents = application.documents.all()
    serializer = ApplicationDocumentSerializer(
        documents, 
        many=True, 
        context={'request': request}
    )
    
    # Group documents by type for easier frontend handling
    grouped_documents = {}
    for doc in serializer.data:
        doc_type = doc['document_type']
        if doc_type not in grouped_documents:
            grouped_documents[doc_type] = []
        grouped_documents[doc_type].append(doc)
    
    return Response({
        'documents': serializer.data,
        'grouped': grouped_documents,
        'total_count': len(serializer.data),
        'has_required': application.has_required_documents
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_application_document(request, document_id):
    """Delete a document (only by applicant who owns it)"""
    try:
        document = ApplicationDocument.objects.get(
            id=document_id,
            application__applicant=request.user
        )
        document.delete()
        return Response(
            {'success': True, 'message': 'Document deleted'},
            status=status.HTTP_200_OK
        )
    except ApplicationDocument.DoesNotExist:
        return Response(
            {'error': 'Document not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class ApplicantApplicationListView(generics.ListAPIView):
    """Applicants can see their own applications"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'applicant':
            return Application.objects.filter(
                applicant=self.request.user
            ).select_related('job', 'applicant').prefetch_related('documents')
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
            ).select_related('job', 'applicant').prefetch_related('documents')
        return Application.objects.none()


class ApplicationDetailView(generics.RetrieveAPIView):
    """View single application with all documents"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'applicant':
            return Application.objects.filter(
                applicant=user
            ).select_related('job', 'applicant').prefetch_related('documents')
        elif user.user_type == 'hr':
            return Application.objects.filter(
                job__posted_by=user
            ).select_related('job', 'applicant').prefetch_related('documents')
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


# ============= OPTIONS VIEWS =============

class EducationOptionsView(APIView):
    """Returns all education options grouped by category"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = EducationCategory.objects.filter(
            is_active=True
        ).prefetch_related('programs')
        serializer = EducationCategorySerializer(categories, many=True)
        return Response(serializer.data)


class EligibilityOptionsView(APIView):
    """
    Returns all eligibility options grouped by category
    Includes both Civil Service Eligibility AND Board Licenses
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = EligibilityCategory.objects.filter(
            is_active=True
        ).prefetch_related('types')
        serializer = EligibilityCategorySerializer(categories, many=True)
        
        # Separate Civil Service from Board Licenses for frontend
        civil_service = []
        board_licenses = []
        
        for category in serializer.data:
            if category.get('is_board_license'):
                board_licenses.append(category)
            else:
                civil_service.append(category)
        
        return Response({
            'all_categories': serializer.data,
            'civil_service': civil_service,
            'board_licenses': board_licenses
        })