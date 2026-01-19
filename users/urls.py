from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterViewSet, EngineerProfileViewSet, AdminImpersonationViewSet

router = DefaultRouter()
router.register(r'profiles', EngineerProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', UserRegisterViewSet.as_view({'post': 'register'}), name='user-register'),
    path('admin/impersonate/<int:pk>/impersonate/', AdminImpersonationViewSet.as_view({'post': 'impersonate'}), name='admin-impersonate'),
    path('', include(router.urls)),
]