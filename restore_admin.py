#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engineer_connect.settings')
django.setup()

from users.models import CustomUser
from django.contrib.auth.models import Permission

# Get admin user
admin = CustomUser.objects.get(username='admin')

# Get all permissions
all_permissions = Permission.objects.all()

# Add all permissions to admin
admin.user_permissions.set(all_permissions)

print(f"Admin now has {admin.user_permissions.count()} permissions")
print("Admin rights restored!")
