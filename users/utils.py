from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user, code):
    try:
        send_mail(
            subject='Your Engineer Konnect Verification Code',
            message=f'Your verification code is: {code}\n\nThis code expires in 10 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        # Don't raise - allow registration to proceed even if email fails

def send_verification_sms(phone, code):
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'Your Engineer Konnect verification code is: {code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
        logger.info(f"Verification SMS sent to {phone}")
    except Exception as e:
        logger.error(f"Failed to send verification SMS to {phone}: {str(e)}")
        # Don't raise - allow registration to proceed even if SMS fails