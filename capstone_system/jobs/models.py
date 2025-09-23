from django.db import models
from accounts.models import User

class JobPosting(models.Model):
    DEPARTMENT_CHOICES = [
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (5+ years)'),
    ]
    
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    location = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.department}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    # Job and Personal Info
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Professional Information
    current_position = models.CharField(max_length=200, blank=True)
    years_of_experience = models.PositiveIntegerField()
    expected_salary = models.CharField(max_length=100, blank=True)
    
    # Documents
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    
    # Additional Info
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    why_interested = models.TextField()
    availability = models.CharField(max_length=100)
    
    # System Fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # OCR Results (for future implementation)
    ocr_extracted_text = models.TextField(blank=True)
    ocr_processed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['job', 'email']  # Prevent duplicate applications
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.job.title}"