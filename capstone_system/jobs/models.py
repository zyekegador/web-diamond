from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os


# File validation
def validate_file_size(file):
    """Validate file size - max 10MB"""
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError(f'File size exceeds 10MB. Current size: {file.size / (1024*1024):.2f}MB')


# Upload path functions
def get_document_upload_path(instance, filename):
    """
    Generate upload path: applications/job_X/applicant_Y/document_type/filename
    """
    application = instance.application
    job_folder = f"job_{application.job.id}_{slugify(application.job.title)}"
    applicant_folder = f"applicant_{application.applicant.id}_{slugify(application.applicant.get_full_name())}"
    doc_type_folder = instance.document_type
    
    # Clean filename
    name, ext = os.path.splitext(filename)
    safe_name = slugify(name)
    safe_filename = f"{safe_name}{ext.lower()}"
    
    return os.path.join('applications', job_folder, applicant_folder, doc_type_folder, safe_filename)


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('permanent', 'Permanent'),
        ('casual', 'Casual'),
        ('contractual', 'Contractual'),
        ('coterminous', 'Coterminous'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Position Title")
    place_of_assignment = models.CharField(max_length=300)
    plantilla_item_no = models.CharField(max_length=50, blank=True)
    salary_job_grade = models.CharField(max_length=10, blank=True)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Job Details
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='permanent')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Requirements
    education_requirement = models.TextField(help_text="e.g., Bachelor's Degree relevant to the job")
    training_requirement = models.CharField(max_length=200, help_text="e.g., 16 hours of relevant training")
    experience_requirement = models.CharField(max_length=200, help_text="e.g., 3 years of relevant experience")
    eligibility_requirement = models.TextField(help_text="e.g., Career Service Professional / Second Level Eligibility OR Board License")
    competency_requirement = models.TextField(blank=True, help_text="Optional preferred qualifications")
    
    # Relations
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posted_jobs',
        limit_choices_to={'user_type': 'hr'}
    )
    
    education_levels = models.ManyToManyField(
        'EducationLevel',
        related_name='jobs',
        blank=True
    )
    eligibility_types = models.ManyToManyField(
        'EligibilityType',
        related_name='jobs',
        blank=True,
        help_text="Can include Civil Service AND/OR Board Licenses"
    )
    
    # Metadata
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Posting Date")
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(verbose_name="Closing Date")
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.deadline and self.deadline < timezone.now().date():
            self.status = "closed"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id or ''}")
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.create_application_folder()
    
    def create_application_folder(self):
        """Create base folder for job applications"""
        folder_path = self.get_job_folder_path()
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def get_job_folder_path(self):
        """Get absolute path for job folder"""
        folder_name = f"job_{self.id}_{slugify(self.title)}"
        return os.path.join(settings.MEDIA_ROOT, 'applications', folder_name)
    
    @property
    def applications_count(self):
        return self.applications.count()
    
    @property
    def is_open(self):
        return self.status == 'open' and self.deadline >= timezone.now().date()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['deadline']),
        ]


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='applications',
        limit_choices_to={'user_type': 'applicant'}
    )
    
    # Letter of Intent
    letter_of_intent = models.TextField(
        help_text="Indicate position, item number, and place of assignment"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True, help_text="HR notes")
    
    # Automated screening results
    screening_score = models.IntegerField(null=True, blank=True, help_text="Automated screening score 0-100")
    screening_result = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        choices=[
            ('highly_qualified', 'Highly Qualified'),
            ('qualified', 'Qualified'),
            ('not_qualified', 'Not Qualified'),
        ]
    )
    screening_details = models.JSONField(null=True, blank=True, help_text="Detailed screening breakdown")
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    
    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        if is_new:
            # Ensure job folder exists
            job_folder = self.job.get_job_folder_path()
            if not os.path.exists(job_folder):
                self.job.create_application_folder()
            
            # Create applicant folder structure
            applicant_name = slugify(f"{self.applicant.first_name}_{self.applicant.last_name}")
            applicant_folder = os.path.join(
                job_folder,
                f"applicant_{self.applicant.id}_{applicant_name}"
            )
            
            # Create document type folders matching CSC requirements
            doc_types = [
                'letter_of_intent',
                'pds',
                'wes',
                'performance_rating',
                'eligibility_license',
                'transcript',
                'training_certificates',
                'other'
            ]
            for doc_type in doc_types:
                os.makedirs(os.path.join(applicant_folder, doc_type), exist_ok=True)
        
        super().save(*args, **kwargs)
    
    @property
    def has_required_documents(self):
        """Check if all required documents are uploaded"""
        required_docs = ['pds', 'wes', 'eligibility_license', 'transcript']
        return all(
            self.documents.filter(document_type=doc_type).exists() 
            for doc_type in required_docs
        )
    
    @property
    def documents_count(self):
        return self.documents.count()
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', '-applied_at']),
            models.Index(fields=['screening_result']),
        ]


class ApplicationDocument(models.Model):
    """Document storage matching CSC requirements"""
    
    DOCUMENT_TYPES = [
        ('letter_of_intent', 'Letter of Intent'),
        ('pds', 'Personal Data Sheet (CS Form 212)'),
        ('wes', 'Work Experience Sheet'),
        ('performance_rating', 'Performance Rating (if applicable)'),
        ('eligibility_license', 'Eligibility Certificate / Board License'),
        ('transcript', 'Transcript of Records'),
        ('training_certificates', 'Training Certificates'),
        ('other', 'Other Supporting Documents'),
    ]
    
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=get_document_upload_path,
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])
        ]
    )
    
    # OCR-specific fields (for PDS, WES, Eligibility/License, Transcript)
    ocr_processed = models.BooleanField(default=False)
    ocr_data = models.JSONField(null=True, blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    ocr_error = models.TextField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.document_name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            if not self.document_name:
                self.document_name = self.file.name
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def requires_ocr(self):
        """Documents that should be processed with OCR"""
        return self.document_type in ['pds', 'wes', 'eligibility_license', 'transcript']
    
    class Meta:
        ordering = ['document_type', '-uploaded_at']
        indexes = [
            models.Index(fields=['application', 'document_type']),
            models.Index(fields=['document_type', 'ocr_processed']),
        ]


# Education Models
class EducationCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Education Categories"
    
    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    category = models.ForeignKey(
        EducationCategory, 
        on_delete=models.CASCADE, 
        related_name='programs'
    )
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return self.name


# Eligibility Models
class EligibilityCategory(models.Model):
    """Categories: Civil Service Eligibility, Professional Board Licenses, etc."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_board_license = models.BooleanField(
        default=False, 
        help_text="True for PRC Board Licenses, False for Civil Service"
    )
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Eligibility Categories"
    
    def __str__(self):
        return self.name


class EligibilityType(models.Model):
    """Specific eligibility types: CSC Professional, PRC Engineer, etc."""
    category = models.ForeignKey(
        EligibilityCategory, 
        on_delete=models.CASCADE, 
        related_name='types'
    )
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return self.name