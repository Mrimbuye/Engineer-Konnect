from django.contrib.auth.models import User
from django.db import models

class EngineerProfile(models.Model):
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    company = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    skills = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    
    # New fields
    engineer_type = models.CharField(max_length=50, choices=ENGINEER_TYPE_CHOICES, default='professional')
    academic_qualifications = models.TextField(blank=True, help_text="e.g., Bachelor's in Mechanical Engineering, Master's in Civil Engineering")
    country_of_practice = models.CharField(max_length=100, blank=True)
    postal_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    certifications = models.TextField(blank=True, help_text="Professional certifications and licenses")
    professional_associations = models.TextField(blank=True, help_text="Member of professional bodies")
    portfolio_url = models.URLField(blank=True, null=True, help_text="Link to your portfolio or website")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = 'engineer_profiles'