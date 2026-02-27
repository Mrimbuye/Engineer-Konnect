import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','engineer_connect.settings')
django.setup()
from django.test import Client
from django.conf import settings
# allow testserver hostname for the test
settings.ALLOWED_HOSTS.append('testserver')
client = Client()
resp = client.post('/api/users/register/', data={
    'username':'testuser','email':'test@example.com','password':'abc123','password2':'abc123',
    'send_email': True,
}, content_type='application/json')
print('status',resp.status_code)
print(resp.content)
