# Account Verification Setup Guide

## Overview
The application now uses a modern verification system with email delivery (via API) and SMS delivery (via Vonage API).

---

## ✅ Current Setup

### Development Mode (DEBUG=True)
- **Email**: Uses Console Backend - verification codes are printed to console/logs
- **SMS**: Logs codes to console (Vonage API ready for prod)
- **Test Codes**: Returned in API response for easy testing

### Production Mode (DEBUG=False)
- **Email**: Requires SMTP configuration (SendGrid, AWS SES, Gmail, etc.)
- **SMS**: Uses Vonage API (requires credentials)

---

## 🧪 Testing the Flow

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Register a New Account
**Option A: Via Web UI**
- Go to `http://localhost:8000/register/`
- Fill in the form and submit
- **✅ SUCCESS**: You'll see the verification code displayed on the confirmation screen

**Option B: Via API (for automated testing)**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+1234567890",
    "send_email": true,
    "send_sms": false
  }'
```

**API Response (DEBUG mode):**
```json
{
  "message": "Account created. Please verify your account.",
  "email": "test@example.com",
  "debug_info": {
    "email_sent": true,
    "sms_sent": false,
    "code_for_testing": "123456"
  }
}
```

### Step 3: Verify the Account
**Option A: Via Web UI**
- Go to `http://localhost:8000/verify/?email=test@example.com`
- Enter the code shown on registration screen
- Click "Verify Account"

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/users/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "code": "123456"
  }'
```

### Step 4: Check Console Output
In DEBUG mode, you'll also see the code printed to the server console:
```
============================================================
[VERIFICATION CODE FOR test@example.com]
Code: 123456
============================================================
```

---

## 📧 Email Configuration

### Development (Console Backend)
No configuration needed! Codes print to console.

### Production (Real Email Delivery)

#### Option 1: Gmail (Simple)
```bash
# Set environment variables
export EMAIL_HOST_USER="your@gmail.com"
export EMAIL_HOST_PASSWORD="your_app_specific_password"
export DEBUG=False
```

#### Option 2: SendGrid (Recommended)
```bash
# Install sendgrid backend
pip install sendgrid-django

# Set environment variables
export EMAIL_BACKEND=sendgrid_backend.SendgridBackend
export SENDGRID_API_KEY=your_sendgrid_key
export DEBUG=False
```

#### Option 3: AWS SES
```bash
# Set environment variables
export EMAIL_BACKEND=django_amazon_ses
export AWS_SES_REGION_NAME=us-east-1
export AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export DEBUG=False
```

---

## 📱 SMS Configuration (Vonage)

### Setup
1. Sign up at https://dashboard.nexmo.com/
2. Get API Key and API Secret from dashboard
3. Set environment variables:

```bash
export VONAGE_API_KEY=your_api_key
export VONAGE_API_SECRET=your_api_secret
export VONAGE_FROM_NUMBER=YourBrand
export DEBUG=False
```

### Test SMS (with credentials)
The SMS service will automatically send via Vonage when DEBUG=False and credentials are set.

---

## 🔄 Resend Verification Code

Users can request a new code if they didn't receive it.

**Via Web UI:**
- Go to verify page
- Click "Resend Code" button
- Code will be resent to email (and SMS if requested)

**Via API:**
```bash
curl -X POST http://localhost:8000/api/users/resend-code/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "send_email": true,
    "send_sms": false
  }'
```

---

## ⏱️ Code Expiration

- Verification codes expire after **10 minutes**
- Users must verify within this timeframe
- After expiration, they can request a new code

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Configure EMAIL_BACKEND with real SMTP provider
- [ ] Set EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
- [ ] Configure Vonage credentials (VONAGE_API_KEY, VONAGE_API_SECRET)
- [ ] Test registration flow end-to-end
- [ ] Verify emails are being delivered
- [ ] Verify SMS messages are being sent (if enabled)
- [ ] Monitor logs for any delivery issues

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/users/register/` | POST | Create account & send verification code |
| `/api/users/verify/` | POST | Verify account with code |
| `/api/users/resend-code/` | POST | Resend verification code |

---

## 🐛 Troubleshooting

### "No verification code received"
1. Check server console for errors
2. Ensure email backend is configured
3. In DEBUG mode, code should print to console

### "Invalid verification code"
1. Verify code was entered correctly
2. Check if code has expired (max 10 minutes)
3. Request a new code and try again

### "Email not working in production"
1. Verify SMTP credentials are correct
2. Check email logs for bounce messages
3. Ensure sender email is authorized
4. Test with `python manage.py shell` and `django.core.mail.send_mail()`

### "SMS not sending"
1. Verify Vonage API credentials
2. Ensure phone number is in correct format (+country code)
3. Check Vonage dashboard for balance/errors
4. Verify DEBUG=False in production

---

## 📝 Code Changes Summary

- ✅ Replaced Twilio with Vonage SMS API
- ✅ Added email console backend for DEBUG mode
- ✅ Created `users/sms_service.py` module
- ✅ Added resend verification code endpoint
- ✅ Improved API responses with debug info
- ✅ Enhanced frontend UX with visible test codes
- ✅ Added "Resend Code" button to verify page

---

## 🎯 Next Steps

1. Test the flow locally in DEBUG mode ✓
2. Deploy to production
3. Configure production email provider
4. Configure Vonage API credentials
5. Monitor verification metrics
6. Iterate based on user feedback
