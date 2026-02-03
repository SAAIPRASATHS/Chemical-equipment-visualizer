import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create admin user
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print('✅ Admin user created successfully!')
    print('Username: admin')
    print('Password: admin123')
else:
    print('⚠️ Admin user already exists')

# Create a regular user for testing
if not User.objects.filter(username='testuser').exists():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role='viewer'
    )
    print('✅ Test user created successfully!')
    print('Username: testuser')
    print('Password: testpass123')
else:
    print('⚠️ Test user already exists')
