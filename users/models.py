from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string


class CustomUser(AbstractUser):
    SPECIALIZATION_CHOICES = [
        ('software', 'Software Engineering'),
        ('civil', 'Civil Engineering'),
        ('mechanical', 'Mechanical Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('chemical', 'Chemical Engineering'),
        ('other', 'Other'),
    ]

    ENGINEER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('graduate', 'Graduate'),
        ('professional', 'Professional'),
        ('consulting', 'Consulting'),
    ]

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    # Verification fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField(blank=True, null=True)

    # Profile fields (merged from EngineerProfile)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True)
    company = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list)
    engineer_type = models.CharField(max_length=50, choices=ENGINEER_TYPE_CHOICES, default='professional')
    academic_qualifications = models.TextField(blank=True)
    country_of_practice = models.CharField(max_length=100, blank=True)
    postal_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    certifications = models.TextField(blank=True)
    professional_associations = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True, null=True)

    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        from django.utils import timezone
        self.verification_code_created_at = timezone.now()
        self.save()
        return self.verification_code

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        db_table = 'custom_users'