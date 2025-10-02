from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os


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
    
    # New structured requirements
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
        # Generate slug if not exists
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id or ''}")
        
        # Check if this is a new job
        is_new = self.pk is None
        
        # Save the job first
        super().save(*args, **kwargs)
        
        # Create folder structure for new jobs
        if is_new:
            self.create_application_folder()
    
    def create_application_folder(self):
        """Create base folder for job applications"""
        folder_path = self.get_job_folder_path()
        os.makedirs(folder_path, exist_ok=True)
        
        # Create a README file in the job folder
        readme_path = os.path.join(folder_path, 'README.txt')
        try:
            with open(readme_path, 'w') as f:
                f.write(f"Job: {self.title}\n")
                f.write(f"Job ID: {self.id}\n")
                f.write(f"Created: {self.created_at}\n")
                f.write(f"Deadline: {self.deadline}\n")
                f.write(f"\nThis folder contains all applications for this job posting.\n")
        except Exception as e:
            print(f"Could not create README: {e}")
        
        return folder_path
    
    def get_job_folder_path(self):
        """Get absolute path for job folder"""
        folder_name = f"job_{self.id}_{slugify(self.title)}"
        return os.path.join(settings.MEDIA_ROOT, 'applications', folder_name)
    
    def get_job_folder_relative(self):
        """Get relative path for URLs"""
        folder_name = f"job_{self.id}_{slugify(self.title)}"
        return os.path.join('applications', folder_name)
    
    class Meta:
        ordering = ['-created_at']


# ===========================================
# Helper functions for file upload paths
# ===========================================

def get_application_upload_path(instance, filename, file_type):
    """
    Generate nested upload path for application files
    Path: applications/job_{id}_{title}/applicant_{id}_{name}/{file_type}/filename
    """
    # Get job folder
    job_folder = instance.job.get_job_folder_relative()
    
    # Create applicant folder name
    applicant_name = slugify(f"{instance.applicant.first_name}_{instance.applicant.last_name}")
    applicant_folder = f"applicant_{instance.applicant.id}_{applicant_name}"
    
    # Clean filename
    name, ext = os.path.splitext(filename)
    safe_name = slugify(name)
    safe_filename = f"{safe_name}{ext.lower()}"
    
    # Complete path
    return os.path.join(job_folder, applicant_folder, file_type, safe_filename)


def resume_upload_path(instance, filename):
    """Upload path for resume/CV files"""
    return get_application_upload_path(instance, filename, 'resume')


def pds_upload_path(instance, filename):
    """Upload path for Personal Data Sheet files"""
    return get_application_upload_path(instance, filename, 'pds')


def certificates_upload_path(instance, filename):
    """Upload path for certificates and supporting documents"""
    return get_application_upload_path(instance, filename, 'certificates')


# ===========================================
# Application Model
# ===========================================

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
    
    # Personal Information
    cover_letter = models.TextField()
    
    # Document uploads with nested folder structure
    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx']
        )],
        help_text="Accepted formats: PDF, DOC, DOCX (Max 5MB)"
    )
    
    pds = models.FileField(
        upload_to=pds_upload_path,
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx']
        )],
        help_text="Personal Data Sheet (Max 5MB)"
    )
    
    certificates = models.FileField(
        upload_to=certificates_upload_path,
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'zip', 'rar']
        )],
        help_text="Certificates (PDF or ZIP/RAR archive, Max 10MB)"
    )
    
    # Application status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)  # HR notes
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    
    def save(self, *args, **kwargs):
        """Create applicant folder structure when application is created"""
        is_new = not self.pk
        
        if is_new:
            # Ensure job folder exists
            job_folder = self.job.get_job_folder_path()
            if not os.path.exists(job_folder):
                self.job.create_application_folder()
            
            # Create applicant folder structure
            applicant_name = slugify(
                f"{self.applicant.first_name}_{self.applicant.last_name}"
            )
            applicant_folder = os.path.join(
                job_folder,
                f"applicant_{self.applicant.id}_{applicant_name}"
            )
            
            # Create subfolders for each document type
            for doc_type in ['resume', 'pds', 'certificates']:
                doc_folder = os.path.join(applicant_folder, doc_type)
                os.makedirs(doc_folder, exist_ok=True)
            
            # Create applicant info file
            info_path = os.path.join(applicant_folder, 'applicant_info.txt')
            try:
                with open(info_path, 'w') as f:
                    f.write(f"Applicant: {self.applicant.first_name} {self.applicant.last_name}\n")
                    f.write(f"Email: {self.applicant.email}\n")
                    f.write(f"Applied: {timezone.now()}\n")
            except Exception as e:
                print(f"Could not create applicant info: {e}")
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Clean up files when application is deleted"""
        # Delete files
        if self.resume:
            self.resume.delete(save=False)
        if self.pds:
            self.pds.delete(save=False)
        if self.certificates:
            self.certificates.delete(save=False)
        
        super().delete(*args, **kwargs)
    
    def get_applicant_folder_path(self):
        """Get the full path to the applicant's folder"""
        job_folder = self.job.get_job_folder_path()
        applicant_name = slugify(
            f"{self.applicant.first_name}_{self.applicant.last_name}"
        )
        return os.path.join(
            job_folder,
            f"applicant_{self.applicant.id}_{applicant_name}"
        )
    
    @property
    def has_all_documents(self):
        """Check if all required documents are uploaded"""
        return bool(self.resume)  # Only resume is required based on your model
    
    @property
    def documents_count(self):
        """Count how many documents have been uploaded"""
        count = 0
        if self.resume:
            count += 1
        if self.pds:
            count += 1
        if self.certificates:
            count += 1
        return count
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']


# =====================
# Education Models
# =====================

class EducationCategory(models.Model):
    """Categories for grouping education levels"""
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Education Categories"
    
    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """Specific degree programs"""
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


# =====================
# Eligibility Models
# =====================

class EligibilityCategory(models.Model):
    """Categories for eligibility types"""
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
    """Specific eligibility requirements"""
    category = models.ForeignKey(
        EligibilityCategory, 
        on_delete=models.CASCADE, 
        related_name='types'
    )
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, blank=True)  # e.g., "RA 1080"
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return self.name