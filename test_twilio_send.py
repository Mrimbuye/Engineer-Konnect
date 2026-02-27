#!/usr/bin/env python3
"""Quick test script to send an SMS using environment TWILIO_* vars.

Usage:
  Set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
  TWILIO_PHONE_NUMBER, and TEST_SMS_TO (the recipient phone number).

  Then run:
    python test_twilio_send.py

The script prints the message SID on success or the error on failure.
"""
import os
import sys

try:
    from twilio.rest import Client
except Exception as e:
    print('Twilio package not installed. Run: pip install twilio')
    sys.exit(1)

def main():
    sid = os.environ.get('TWILIO_ACCOUNT_SID')
    token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_num = os.environ.get('TWILIO_PHONE_NUMBER')
    to = os.environ.get('TEST_SMS_TO') or os.environ.get('MY_PHONE')
    body = os.environ.get('TEST_SMS_BODY', 'Test SMS from Engineer Konnect')

    if not sid or not token or not from_num or not to:
        print('Missing required env vars. Please set:')
        print('  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TEST_SMS_TO')
        sys.exit(2)

    client = Client(sid, token)
    try:
        msg = client.messages.create(body=body, from_=from_num, to=to)
        print('Message queued/sent. SID:', msg.sid)
        print('Status:', getattr(msg, 'status', 'unknown'))
    except Exception as e:
        print('Failed to send SMS:', repr(e))
        sys.exit(3)

if __name__ == '__main__':
    main()
