from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id or ''}")
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']


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
    
    # Document uploads
    resume = models.FileField(upload_to='resumes/')
    pds = models.FileField(upload_to='pds/', blank=True, null=True)  # Personal Data Sheet
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    # Application status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)  # HR notes
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    
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
