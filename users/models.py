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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    company = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    skills = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = 'engineer_profiles'