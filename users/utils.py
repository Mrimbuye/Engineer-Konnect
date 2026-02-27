from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client  # pip install twilio

def send_verification_email(user, code):
    send_mail(
        subject='Your Engineer Konnect Verification Code',
        message=f'Your verification code is: {code}\n\nThis code expires in 10 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_verification_sms(phone, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f'Your Engineer Konnect verification code is: {code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )