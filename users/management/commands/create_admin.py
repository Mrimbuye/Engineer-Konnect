from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser admin account for testing'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            admin = User.objects.get(username='admin')
            self.stdout.write(f'Username: admin, is_staff: {admin.is_staff}')
        else:
            admin = User.objects.create_superuser('admin', 'admin@engineer-konnect.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
            self.stdout.write(f'Username: admin')
            self.stdout.write(f'Password: admin123')
            self.stdout.write(f'Email: admin@engineer-konnect.com')
