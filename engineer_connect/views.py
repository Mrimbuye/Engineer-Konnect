from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings
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

    try:
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

        # log the code; this is useful for server-side monitoring
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Generated verification code for {user.email}: {code}")

        email_sent = False
        sms_sent = False

        if data.get('send_email', True):
            email_sent = send_verification_email(user, code)

        if data.get('send_sms') and user.phone:
            from users.sms_service import send_verification_sms as sms_send
            sms_sent = sms_send(user.phone, code)

        resp = {
            'message': 'Account created. Please verify your account.',
            'email': user.email,
            'debug_info': {
                'email_sent': email_sent,
                'sms_sent': sms_sent,
                'code_for_testing': code if getattr(settings, 'DEBUG', False) else None
            } if getattr(settings, 'DEBUG', False) else {}
        }
        return Response(resp, status=201)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Registration error: {str(e)}")
        return Response({'error': [str(e)]}, status=500)


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


@api_view(['POST'])
@permission_classes([AllowAny])
def api_resend_verification_code(request):
    """Resend verification code to email and/or SMS"""
    email = request.data.get('email')
    phone = request.data.get('phone')
    send_email = request.data.get('send_email', True)
    send_sms = request.data.get('send_sms', False)

    if not email:
        return Response({'error': 'Email is required.'}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    if user.is_verified:
        return Response({'error': 'User is already verified.'}, status=400)

    # Generate new verification code
    code = user.generate_verification_code()
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Resent verification code for {user.email}: {code}")

    email_sent = False
    sms_sent = False

    if send_email:
        email_sent = send_verification_email(user, code)

    if send_sms and (phone or user.phone):
        from users.sms_service import send_verification_sms as sms_send
        target_phone = phone or user.phone
        sms_sent = sms_send(target_phone, code)

    resp = {
        'message': 'Verification code resent successfully.',
        'debug_info': {
            'email_sent': email_sent,
            'sms_sent': sms_sent,
            'code_for_testing': code if getattr(settings, 'DEBUG', False) else None
        } if getattr(settings, 'DEBUG', False) else {}
    }
    return Response(resp, status=200)