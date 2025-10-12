from rest_framework import serializers
from .models import (
    Job, Application, ApplicationDocument,
    EducationCategory, EducationLevel, 
    EligibilityCategory, EligibilityType
)
from accounts.serializers import UserSerializer


# Education & Eligibility Serializers
class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'name', 'abbreviation']


class EducationCategorySerializer(serializers.ModelSerializer):
    programs = EducationLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = EducationCategory
        fields = ['id', 'name', 'icon', 'programs']


class EligibilityTypeSerializer(serializers.ModelSerializer):
    is_board_license = serializers.BooleanField(source='category.is_board_license', read_only=True)
    
    class Meta:
        model = EligibilityType
        fields = ['id', 'name', 'code', 'description', 'is_board_license']


class EligibilityCategorySerializer(serializers.ModelSerializer):
    types = EligibilityTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = EligibilityCategory
        fields = ['id', 'name', 'description', 'is_board_license', 'types']


# Document Serializers
class ApplicationDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = ApplicationDocument
        fields = [
            'id', 'document_type', 'document_type_display', 'document_name',
            'file', 'file_url', 'file_size', 'file_size_display',
            'ocr_processed', 'ocr_confidence', 'uploaded_at'
        ]
        read_only_fields = ['id', 'file_size', 'ocr_processed', 'ocr_confidence', 'uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size_display(self, obj):
        return f"{obj.file_size_mb} MB"


class ApplicationDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['document_type', 'file']
    
    def validate_file(self, value):
        # Additional file validation
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF, JPG, and PNG files are allowed.")
        return value


# Job Serializers
class JobSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    applications_count = serializers.IntegerField(source='applications.count', read_only=True)
    education_levels = EducationLevelSerializer(many=True, read_only=True)
    eligibility_types = EligibilityTypeSerializer(many=True, read_only=True)
    is_open = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'place_of_assignment', 'plantilla_item_no',
            'salary_job_grade', 'monthly_salary', 'description', 'job_type',
            'education_requirement', 'training_requirement', 'experience_requirement',
            'eligibility_requirement', 'competency_requirement',
            'education_levels', 'eligibility_types',
            'status', 'posted_by', 'created_at', 'deadline', 
            'applications_count', 'is_open'
        ]
        read_only_fields = ['id', 'posted_by', 'created_at']
    
    def get_applications_count(self, obj):
        # Try to use annotated count first, fallback to query
        if hasattr(obj, 'applications_count'):
            return obj.applications_count
        return obj.applications.count()


class JobCreateSerializer(serializers.ModelSerializer):
    education_level_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    eligibility_type_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Job
        fields = [
            'title', 'place_of_assignment', 'plantilla_item_no',
            'salary_job_grade', 'monthly_salary', 'description', 'job_type',
            'education_requirement', 'training_requirement', 'experience_requirement',
            'eligibility_requirement', 'competency_requirement',
            'education_level_ids', 'eligibility_type_ids', 'deadline'
        ]
    
    def create(self, validated_data):
        education_ids = validated_data.pop('education_level_ids', [])
        eligibility_ids = validated_data.pop('eligibility_type_ids', [])
        
        job = Job.objects.create(**validated_data)
        
        if education_ids:
            job.education_levels.set(education_ids)
        if eligibility_ids:
            job.eligibility_types.set(eligibility_ids)
        
        return job
    
    def update(self, instance, validated_data):
        education_ids = validated_data.pop('education_level_ids', None)
        eligibility_ids = validated_data.pop('eligibility_type_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if education_ids is not None:
            instance.education_levels.set(education_ids)
        if eligibility_ids is not None:
            instance.eligibility_types.set(eligibility_ids)
        
        return instance


# Application Serializers
class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    documents = ApplicationDocumentSerializer(many=True, read_only=True)
    has_required_documents = serializers.BooleanField(read_only=True)
    screening_result_display = serializers.CharField(source='get_screening_result_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'applicant', 'application_letter',
            'status', 'notes', 'screening_score', 'screening_result',
            'screening_result_display', 'screening_details',
            'documents', 'has_required_documents',
            'applied_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'applicant', 'screening_score', 'screening_result',
            'screening_details', 'applied_at', 'updated_at'
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """For initial application submission"""
    
    class Meta:
        model = Application
        fields = ['job', 'application_letter']
    
    def validate(self, attrs):
        request = self.context.get('request')
        job = attrs.get('job')
        
        # Check if user already applied
        if Application.objects.filter(job=job, applicant=request.user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        # Check if job is open
        if not job.is_open:
            raise serializers.ValidationError("This job is no longer accepting applications.")
        
        return attrs


class ApplicationWithDocumentsSerializer(serializers.Serializer):
    """For complete application submission with documents"""
    job_id = serializers.IntegerField()
    application_letter = serializers.FileField()
    
    # Required documents
    pds_file = serializers.FileField()
    wes_file = serializers.FileField()
    eligibility_license_file = serializers.FileField()
    transcript_file = serializers.FileField()
    
    # Optional documents
    performance_rating_file = serializers.FileField(required=False)
    training_certificates_files = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )
    other_files = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )
    
    def validate_application_letter(self, value):
        """Validate application letter file type"""
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Application letter must be PDF or Word document (.pdf, .doc, .docx)"
            )
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        job_id = attrs.get('job_id')
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError("Job not found.")
        
        # Check if user already applied
        if Application.objects.filter(job=job, applicant=request.user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        # Check if job is open
        if not job.is_open:
            raise serializers.ValidationError("This job is no longer accepting applications.")
        
        attrs['job'] = job
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        job = validated_data['job']
        
        # Create application with application_letter file
        application = Application.objects.create(
            job=job,
            applicant=request.user,
            application_letter=validated_data['application_letter']
        )
        
        # Map files to document types
        document_mapping = {
            'pds_file': 'pds',
            'wes_file': 'wes',
            'eligibility_license_file': 'eligibility_license',
            'transcript_file': 'transcript',
            'performance_rating_file': 'performance_rating',
        }
        
        # Upload required and optional single files
        for file_key, doc_type in document_mapping.items():
            if file_key in validated_data:
                ApplicationDocument.objects.create(
                    application=application,
                    document_type=doc_type,
                    file=validated_data[file_key]
                )
        
        # Upload multiple training certificates
        if 'training_certificates_files' in validated_data:
            for cert_file in validated_data['training_certificates_files']:
                ApplicationDocument.objects.create(
                    application=application,
                    document_type='training_certificates',
                    file=cert_file
                )
        
        # Upload other documents
        if 'other_files' in validated_data:
            for other_file in validated_data['other_files']:
                ApplicationDocument.objects.create(
                    application=application,
                    document_type='other',
                    file=other_file
                )
        
        return application


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """For HR to update application status"""
    class Meta:
        model = Application
        fields = ['status', 'notes']