from django.contrib import admin
from .models import (
    Job, Application, ApplicationDocument,
    EducationCategory, EducationLevel,
    EligibilityCategory, EligibilityType
)


# ============= EDUCATION ADMIN =============

@admin.register(EducationCategory)
class EducationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'category', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'abbreviation']
    ordering = ['category__order', 'order', 'name']


# ============= ELIGIBILITY ADMIN =============

@admin.register(EligibilityCategory)
class EligibilityCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_board_license', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_board_license', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(EligibilityType)
class EligibilityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'get_is_board_license', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active', 'category__is_board_license']
    search_fields = ['name', 'code', 'description']
    ordering = ['category__order', 'order', 'name']
    
    def get_is_board_license(self, obj):
        return obj.category.is_board_license
    get_is_board_license.boolean = True
    get_is_board_license.short_description = 'Board License'


# ============= JOB ADMIN =============

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ['applicant', 'status', 'applied_at']
    fields = ['applicant', 'status', 'screening_result', 'applied_at']
    can_delete = False


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'place_of_assignment', 'monthly_salary', 
        'status', 'deadline', 'posted_by', 'applications_count'
    ]
    list_filter = ['status', 'job_type', 'created_at']
    search_fields = ['title', 'place_of_assignment', 'plantilla_item_no']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'applications_count']
    filter_horizontal = ['education_levels', 'eligibility_types']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'place_of_assignment', 'plantilla_item_no',
                'salary_job_grade', 'monthly_salary', 'job_type'
            )
        }),
        ('Job Details', {
            'fields': ('description', 'status', 'deadline')
        }),
        ('Requirements', {
            'fields': (
                'education_requirement', 'training_requirement',
                'experience_requirement', 'eligibility_requirement',
                'competency_requirement'
            )
        }),
        ('Relations', {
            'fields': ('posted_by', 'education_levels', 'eligibility_types')
        }),
        ('Metadata', {
            'fields': ('slug', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ApplicationInline]
    
    def applications_count(self, obj):
        return obj.applications_count
    applications_count.short_description = 'Applications'


# ============= APPLICATION ADMIN =============

class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    readonly_fields = ['document_name', 'file_size_mb', 'ocr_processed', 'uploaded_at']
    fields = ['document_type', 'document_name', 'file', 'file_size_mb', 'ocr_processed', 'uploaded_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'applicant', 'job', 'status', 
        'screening_result', 'screening_score', 
        'has_required_documents', 'applied_at'
    ]
    list_filter = ['status', 'screening_result', 'applied_at']
    search_fields = [
        'applicant__username', 'applicant__email',
        'applicant__first_name', 'applicant__last_name',
        'job__title'
    ]
    readonly_fields = [
        'applied_at', 'updated_at', 'has_required_documents',
        'documents_count', 'screening_details'
    ]
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('job', 'applicant', 'letter_of_intent', 'status')
        }),
        ('Automated Screening', {
            'fields': ('screening_score', 'screening_result', 'screening_details'),
            'classes': ('collapse',)
        }),
        ('HR Notes', {
            'fields': ('notes',)
        }),
        ('Documents', {
            'fields': ('has_required_documents', 'documents_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ApplicationDocumentInline]
    
    def has_required_documents(self, obj):
        return obj.has_required_documents
    has_required_documents.boolean = True
    has_required_documents.short_description = 'Complete Docs'
    
    def documents_count(self, obj):
        return obj.documents_count
    documents_count.short_description = 'Document Count'


# ============= DOCUMENT ADMIN =============

@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'application', 'document_type', 
        'file_size_mb', 'ocr_processed', 'uploaded_at'
    ]
    list_filter = ['document_type', 'ocr_processed', 'uploaded_at']
    search_fields = [
        'application__applicant__username',
        'application__job__title',
        'document_name'
    ]
    readonly_fields = [
        'file_size', 'file_size_mb', 'uploaded_at',
        'ocr_confidence', 'ocr_error'
    ]
    
    fieldsets = (
        ('Document Info', {
            'fields': ('application', 'document_type', 'document_name', 'file')
        }),
        ('File Details', {
            'fields': ('file_size', 'file_size_mb', 'uploaded_at'),
            'classes': ('collapse',)
        }),
        ('OCR Processing', {
            'fields': ('ocr_processed', 'ocr_confidence', 'ocr_data', 'ocr_error'),
            'classes': ('collapse',)
        })
    )
    
    def file_size_mb(self, obj):
        return f"{obj.file_size_mb} MB"
    file_size_mb.short_description = 'File Size'