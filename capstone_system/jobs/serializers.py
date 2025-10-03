from rest_framework import serializers
from .models import Job, Application
from accounts.serializers import UserSerializer
from .models import EducationCategory, EducationLevel, EligibilityCategory, EligibilityType

class JobSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'requirements', 'job_type', 
                  'location', 'salary_range', 'status', 'posted_by', 
                  'created_at', 'updated_at', 'deadline', 'application_count']
        read_only_fields = ['id', 'posted_by', 'created_at', 'updated_at']
    
    def get_application_count(self, obj):
        return obj.applications.count()


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'job_type', 
                  'location', 'salary_range', 'deadline']


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'resume', 
                  'pds', 'certificates', 'status', 'notes', 
                  'applied_at', 'updated_at']
        read_only_fields = ['id', 'applicant', 'applied_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'cover_letter', 'resume', 'pds', 'certificates']
    
    def validate(self, attrs):
        request = self.context.get('request')
        job = attrs.get('job')
        
        # Check if user already applied
        if Application.objects.filter(job=job, applicant=request.user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        # Check if job is open
        if job.status != 'open':
            raise serializers.ValidationError("This job is no longer accepting applications.")
        
        return attrs


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'notes']


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
    class Meta:
        model = EligibilityType
        fields = ['id', 'name', 'code', 'description']


class EligibilityCategorySerializer(serializers.ModelSerializer):
    types = EligibilityTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = EligibilityCategory
        fields = ['id', 'name', 'description', 'types']

class ApplicationSubmissionSerializer(serializers.ModelSerializer):
    """For frontend application form submission"""
    class Meta:
        model = Application
        fields = ['job', 'cover_letter', 'resume', 'pds', 'certificates']
    
    def validate(self, attrs):
        request = self.context.get('request')
        job = attrs.get('job')
        
        # Check if user already applied
        if Application.objects.filter(job=job, applicant=request.user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        # Check if job is open
        if job.status != 'open':
            raise serializers.ValidationError("This job is no longer accepting applications.")
        
        return attrs


class StatusUpdateSerializer(serializers.ModelSerializer):
    """For HR to update status"""
    class Meta:
        model = Application
        fields = ['status', 'notes']