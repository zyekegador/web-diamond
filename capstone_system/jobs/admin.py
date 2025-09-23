from django.contrib import admin
from .models import JobPosting, JobApplication

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'experience_level', 'is_active', 'created_by', 'created_at')
    list_filter = ('department', 'experience_level', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'status', 'applied_at')
    list_filter = ('status', 'job__department', 'applied_at')
    search_fields = ('full_name', 'email', 'job__title')
    list_editable = ('status',)
    readonly_fields = ('applied_at', 'updated_at')