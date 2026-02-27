from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserSerializer, EngineerProfileSerializer, UserRegisterSerializer

class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                # Update specialization and location on the user object
                user.specialization = request.data.get('specialization', 'other')
                user.location = request.data.get('location', '')
                user.save()
                # generate and dispatch verification code
                code = user.generate_verification_code()
                if request.data.get('send_email', True):
                    from users.utils import send_verification_email
                    send_verification_email(user, code)
                if request.data.get('send_sms') and user.phone:
                    from users.utils import send_verification_sms
                    send_verification_sms(user.phone, code)
                response_data = {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                }
                from django.conf import settings
                if getattr(settings, 'DEBUG', False):
                    response_data['verification_code'] = code
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EngineerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = EngineerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
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
            target_user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
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
