from django.contrib import admin
from .models import (
    Job, Application, 
    EducationCategory, EducationLevel,
    EligibilityCategory, EligibilityType
)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'job_type', 'location', 'status', 'posted_by', 'created_at']
    list_filter = ['job_type', 'status', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'job__title']
    readonly_fields = ['applied_at', 'updated_at']

@admin.register(EducationCategory)
class EducationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'abbreviation']
    ordering = ['category__order', 'order', 'name']


@admin.register(EligibilityCategory)
class EligibilityCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']


@admin.register(EligibilityType)
class EligibilityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['category__order', 'order', 'name']