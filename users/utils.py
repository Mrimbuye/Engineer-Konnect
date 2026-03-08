from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user, code):
    """Send verification code via email"""
    try:
        if settings.DEBUG:
            logger.info(f"\n{'='*60}")
            logger.info(f"[VERIFICATION CODE FOR {user.email}]")
            logger.info(f"Code: {code}")
            logger.info(f"{'='*60}\n")
        
        send_mail(
            subject='Your Engineer Konnect Verification Code',
            message=f'Your verification code is: {code}\n\nThis code expires in 10 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {user.email}")
        return True
    except Exception as e:
        error_msg = f"Failed to send verification email to {user.email}: {str(e)}"
        logger.error(error_msg)
        print(f"ERROR: {error_msg}")
        # Don't raise - allow registration to proceed even if email fails
        return False

def send_verification_sms(phone, code):
    """Send verification SMS using Vonage API"""
    from users.sms_service import send_verification_sms as vonage_send_sms
    
    success = vonage_send_sms(phone, code)
    if not success:
        logger.warning(f"SMS delivery status uncertain for {phone}. User can still verify via email.")