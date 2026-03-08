"""
SMS Service Module - Handles sending verification codes via SMS using Vonage API
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_verification_sms(phone_number, code):
    """
    Send verification code via SMS using Vonage API
    
    Args:
        phone_number (str): Recipient phone number in international format (e.g., +1234567890)
        code (str): 6-digit verification code
    
    Returns:
        bool: True if SMS was sent successfully, False otherwise
    """
    
    # In debug mode, just log the code
    if getattr(settings, 'DEBUG', False):
        logger.info(f"[DEBUG MODE] Verification SMS to {phone_number}: {code}")
        print(f"[DEBUG] Verification SMS to {phone_number}: {code}")
        return True
    
    # Get API credentials from settings
    api_key = getattr(settings, 'VONAGE_API_KEY', '')
    api_secret = getattr(settings, 'VONAGE_API_SECRET', '')
    from_number = getattr(settings, 'VONAGE_FROM_NUMBER', 'Engineer')
    
    # Validate credentials are configured
    if not api_key or not api_secret:
        logger.error("Vonage API credentials not configured. Please set VONAGE_API_KEY and VONAGE_API_SECRET.")
        return False
    
    try:
        import vonage
        
        # Create Vonage client
        client = vonage.Client(key=api_key, secret=api_secret)
        
        # Send SMS
        try:
            response = client.sms.send_message({
                "to": phone_number,
                "from": from_number,
                "text": f"Your Engineer Konnect verification code is: {code}\n\nThis code expires in 10 minutes."
            })
            
            # Check if message was sent successfully
            if response["messages"][0]["status"] == "0":
                logger.info(f"Verification SMS sent successfully to {phone_number}")
                return True
            else:
                error_msg = response["messages"][0].get("error-text", "Unknown error")
                logger.error(f"Failed to send SMS to {phone_number}: {error_msg}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending SMS to {phone_number}: {str(e)}")
            return False
            
    except ImportError:
        logger.error("Vonage package not installed. Run: pip install vonage")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in SMS service: {str(e)}")
        return False


def send_sms(phone_number, message):
    """
    Send a generic SMS message using Vonage API
    
    Args:
        phone_number (str): Recipient phone number in international format
        message (str): Message text to send
    
    Returns:
        bool: True if SMS was sent successfully, False otherwise
    """
    
    # In debug mode, just log the message
    if getattr(settings, 'DEBUG', False):
        logger.info(f"[DEBUG MODE] SMS to {phone_number}: {message}")
        print(f"[DEBUG] SMS to {phone_number}: {message}")
        return True
    
    # Get API credentials from settings
    api_key = getattr(settings, 'VONAGE_API_KEY', '')
    api_secret = getattr(settings, 'VONAGE_API_SECRET', '')
    from_number = getattr(settings, 'VONAGE_FROM_NUMBER', 'Engineer')
    
    # Validate credentials are configured
    if not api_key or not api_secret:
        logger.error("Vonage API credentials not configured.")
        return False
    
    try:
        import vonage
        
        # Create Vonage client
        client = vonage.Client(key=api_key, secret=api_secret)
        
        # Send SMS
        try:
            response = client.sms.send_message({
                "to": phone_number,
                "from": from_number,
                "text": message
            })
            
            # Check if message was sent successfully
            if response["messages"][0]["status"] == "0":
                logger.info(f"SMS sent successfully to {phone_number}")
                return True
            else:
                error_msg = response["messages"][0].get("error-text", "Unknown error")
                logger.error(f"Failed to send SMS to {phone_number}: {error_msg}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending SMS to {phone_number}: {str(e)}")
            return False
            
    except ImportError:
        logger.error("Vonage package not installed. Run: pip install vonage")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in SMS service: {str(e)}")
        return False
