from django.contrib import admin
from .models import JobPosting, JobApplication

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'posted_by', 'job_type', 'experience_level', 'is_active', 'views', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'company', 'location', 'posted_by__username')
    readonly_fields = ('views', 'created_at', 'updated_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username')
    readonly_fields = ('applied_at',)

