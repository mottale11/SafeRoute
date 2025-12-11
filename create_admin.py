#!/usr/bin/env python
"""
Standalone script to create admin user.
Can be run during build process or manually.

Set these environment variables:
- ADMIN_USERNAME (default: admin)
- ADMIN_EMAIL (default: admin@saferoute.com)
- ADMIN_PASSWORD (required)
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferoute.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@saferoute.com')
    password = os.environ.get('ADMIN_PASSWORD', None)

    # Check if superuser exists
    if User.objects.filter(is_superuser=True).exists():
        print(f'✅ Superuser already exists. Skipping creation.')
        return

    if not password:
        print('❌ Error: ADMIN_PASSWORD environment variable is required!')
        print('   Set it in Render dashboard: Environment → Add Variable')
        sys.exit(1)

    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Superuser "{username}" created successfully!')
        print(f'   Email: {email}')
        print(f'   Access admin at: /admin/')
    except Exception as e:
        print(f'❌ Error creating superuser: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    create_admin()

