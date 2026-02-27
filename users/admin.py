from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_staff', 'is_active', 'engineer_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('Basic Info', {'fields': ('username', 'email', 'password', 'first_name', 'last_name')}),
        ('Profile', {'fields': ('bio', 'profile_picture', 'phone', 'location')}),
        ('Professional', {'fields': ('specialization', 'company', 'years_experience', 'engineer_type', 'skills')}),
        ('Additional', {'fields': ('academic_qualifications', 'country_of_practice', 'postal_address', 'phone_number', 'certifications', 'professional_associations', 'portfolio_url')}),
        ('Verification', {'fields': ('is_verified', 'verification_code', 'verification_code_created_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

