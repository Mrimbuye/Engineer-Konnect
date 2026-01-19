from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from . import views

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'auth_login': request.build_absolute_uri('/api/auth/login/'),
        'users': request.build_absolute_uri('/api/users/'),
        'discussions': request.build_absolute_uri('/api/discussions/'),
        'jobs': request.build_absolute_uri('/api/jobs/'),
        'messages': request.build_absolute_uri('/api/messages/'),
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', api_root, name='api-root'),
    path('api/auth/login/', obtain_auth_token, name='api_token_auth'),
    path('api/users/', include('users.urls')),
    path('api/discussions/', include('discussions.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/messages/', include('messaging.urls')),
    
    # Frontend pages
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('discussions/', views.discussions, name='discussions'),
    path('jobs/', views.jobs, name='jobs'),
    path('messages/', views.messages, name='messages'),
    path('connections/', views.connections, name='connections'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)