import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','engineer_connect.settings')
django.setup()
from django.test import Client
client = Client()
resp = client.post('/api/users/register/', data={
    'username':'testuser','email':'test@example.com','password':'abc123','password2':'abc123'
}, content_type='application/json')
print('status',resp.status_code)
print(resp.content)
