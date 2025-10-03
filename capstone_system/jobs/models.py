from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os


# File validation
def validate_file_size(file):
    """Validate file size - max 5MB for documents, 10MB for archives"""
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
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
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
        blank=True
    )
    
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True, null=True)
    
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
    
    def get_job_folder_relative(self):
        """Get relative path for URLs"""
        folder_name = f"job_{self.id}_{slugify(self.title)}"
        return os.path.join('applications', folder_name)
    
    @property
    def applications_count(self):
        return self.applications.count()
    
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
    
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
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
            
            # Create document type folders
            doc_types = ['pds', 'graduation_cert', 'eligibility_cert', 'training_cert', 'other']
            for doc_type in doc_types:
                os.makedirs(os.path.join(applicant_folder, doc_type), exist_ok=True)
        
        super().save(*args, **kwargs)
    
    @property
    def has_pds(self):
        return self.documents.filter(document_type='pds').exists()
    
    @property
    def documents_count(self):
        return self.documents.count()
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', '-applied_at']),
        ]


class ApplicationDocument(models.Model):
    """Unified document storage - handles all document types"""
    
    DOCUMENT_TYPES = [
        ('pds', 'PDS - Personal Data Sheet (For OCR)'),
        ('graduation_cert', 'Graduation Certificate'),
        ('eligibility_cert', 'Eligibility Certificate'),
        ('training_cert', 'Training Certificate'),
        ('resume', 'Resume/CV'),
        ('other', 'Other Supporting Document'),
    ]
    
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=get_document_upload_path,
        validators=[validate_file_size]
    )
    
    # OCR-specific fields (only used for PDS documents)
    ocr_processed = models.BooleanField(default=False)
    ocr_data = models.JSONField(null=True, blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    ocr_error = models.TextField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)  # Store in bytes
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.document_name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            if not self.document_name:
                self.document_name = self.file.name
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the file when the record is deleted
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)
    
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
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Eligibility Categories"
    
    def __str__(self):
        return self.name


class EligibilityType(models.Model):
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