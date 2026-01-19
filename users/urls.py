from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterViewSet, EngineerProfileViewSet

router = DefaultRouter()
router.register(r'profiles', EngineerProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', UserRegisterViewSet.as_view({'post': 'register'}), name='user-register'),
    path('', include(router.urls)),
]