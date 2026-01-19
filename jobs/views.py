from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JobPosting, JobApplication
from .serializers import JobPostingSerializer, JobApplicationSerializer

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job=job, applicant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_applications(self, request):
        applications = JobApplication.objects.filter(applicant=request.user)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)