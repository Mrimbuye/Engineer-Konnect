from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import EngineerProfile
from .serializers import UserSerializer, EngineerProfileSerializer, UserRegisterSerializer

class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = EngineerProfile.objects.create(
                user=user,
                specialization=request.data.get('specialization', 'other'),
                location=request.data.get('location', '')
            )
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EngineerProfileViewSet(viewsets.ModelViewSet):
    queryset = EngineerProfile.objects.all()
    serializer_class = EngineerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        profile = EngineerProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        profile = EngineerProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminImpersonationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def impersonate(self, request, pk=None):
        # Only staff/superusers can impersonate
        if not request.user.is_staff:
            return Response(
                {'error': 'Only administrators can impersonate users'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create token for the target user
        token, created = Token.objects.get_or_create(user=target_user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(target_user).data,
            'message': f'You are now impersonating {target_user.first_name} {target_user.last_name}'
        })
