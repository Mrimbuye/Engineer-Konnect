from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from users.utils import send_verification_email, send_verification_sms


# ─────────────────────────────────────────
# PAGE VIEWS
# ─────────────────────────────────────────

@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def register_page(request):
    return render(request, 'register.html')

@require_http_methods(["GET"])
def login_page(request):
    return render(request, 'login.html')

@require_http_methods(["GET"])
def verify_page(request):
    return render(request, 'verify.html')

@require_http_methods(["GET"])
def dashboard(request):
    return render(request, 'dashboard.html')

@require_http_methods(["GET"])
def profile(request):
    return render(request, 'profile.html')

@require_http_methods(["GET"])
def profile_edit(request):
    return render(request, 'profile_edit.html')

@require_http_methods(["GET"])
def discussions(request):
    return render(request, 'discussions.html')

@require_http_methods(["GET"])
def jobs(request):
    return render(request, 'jobs.html')

@require_http_methods(["GET"])
def messages(request):
    return render(request, 'messages.html')

@require_http_methods(["GET"])
def connections(request):
    return render(request, 'connections.html')

@require_http_methods(["GET"])
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    return render(request, 'admin_dashboard.html')


# ─────────────────────────────────────────
# API VIEWS
# ─────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    data = request.data

    if data.get('password') != data.get('password2'):
        return Response({'error': ['Passwords do not match.']}, status=400)

    if not data.get('username'):
        return Response({'error': ['Username is required.']}, status=400)

    if not data.get('email'):
        return Response({'error': ['Email is required.']}, status=400)

    if CustomUser.objects.filter(username=data['username']).exists():
        return Response({'error': ['Username already taken.']}, status=400)

    if CustomUser.objects.filter(email=data['email']).exists():
        return Response({'error': ['Email already registered.']}, status=400)

    user = CustomUser.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        phone=data.get('phone', ''),
        is_verified=False,
        is_active=False,
    )

    code = user.generate_verification_code()

    # log the code; this is useful for server-side monitoring but not shown to clients
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Generated verification code for {user.email}: {code}")

    if data.get('send_email', True):
        send_verification_email(user, code)

    if data.get('send_sms') and user.phone:
        send_verification_sms(user.phone, code)

    resp = {'message': 'Account created. Please verify your account.'}
    return Response(resp, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_verify(request):
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({'error': 'Email and code are required.'}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    if not user.verification_code_created_at:
        return Response({'error': 'No verification code found. Please register again.'}, status=400)

    expiry_time = user.verification_code_created_at + timedelta(minutes=10)
    if timezone.now() > expiry_time:
        return Response({'error': 'Verification code has expired. Please register again.'}, status=400)

    if user.verification_code != code:
        return Response({'error': 'Invalid verification code.'}, status=400)

    user.is_verified = True
    user.is_active = True
    user.verification_code = None
    user.save()

    return Response({'message': 'Account verified successfully! You can now log in.'}, status=200)