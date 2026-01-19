from rest_framework import serializers
from .models import JobPosting, JobApplication
from users.serializers import UserSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    applications = JobApplicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobPosting
        fields = '__all__'