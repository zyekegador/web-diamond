from rest_framework import serializers
from .models import JobPosting, JobApplication

class JobPostingSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'department', 'location', 'experience_level',
            'description', 'requirements', 'salary_range', 'is_active',
            'created_by_username', 'created_at', 'updated_at'
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_department = serializers.CharField(source='job.department', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'job_department',
            'full_name', 'email', 'phone', 'address',
            'current_position', 'years_of_experience', 'expected_salary',
            'resume', 'cover_letter', 'portfolio_url', 'linkedin_url',
            'why_interested', 'availability', 'status', 'applied_at'
        ]
        read_only_fields = ['status', 'applied_at']

# For public job listings (no sensitive info)
class PublicJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'department', 'location', 'experience_level',
            'description', 'requirements', 'salary_range', 'created_at'
        ]