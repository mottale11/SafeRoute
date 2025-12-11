"""
Management command to automatically create a superuser if one doesn't exist.
This can be run during deployment via build.sh or environment variables.

Usage:
    python manage.py create_superuser_auto
    
Or set environment variables:
    ADMIN_USERNAME=admin
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=your_secure_password
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser automatically if one does not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Admin username (or use ADMIN_USERNAME env var)',
            default=os.environ.get('ADMIN_USERNAME', 'admin')
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email (or use ADMIN_EMAIL env var)',
            default=os.environ.get('ADMIN_EMAIL', 'admin@saferoute.com')
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password (or use ADMIN_PASSWORD env var)',
            default=os.environ.get('ADMIN_PASSWORD', None)
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Run non-interactively (requires password via env var or --password)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        noinput = options['noinput']

        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser already exists. Skipping creation.')
            )
            return

        # If no password provided and not in noinput mode, prompt
        if not password and not noinput:
            password = self.get_password_interactive()

        # If still no password, generate a random one
        if not password:
            from django.core.management.utils import get_random_secret_key
            password = get_random_secret_key()[:20]
            self.stdout.write(
                self.style.WARNING(
                    f'No password provided. Generated random password: {password}\n'
                    f'⚠️  IMPORTANT: Save this password! You can change it later in admin panel.'
                )
            )

        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser "{username}" created successfully!\n'
                    f'   Email: {email}\n'
                    f'   Access admin at: /admin/'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )

    def get_password_interactive(self):
        """Get password interactively if possible"""
        import getpass
        try:
            password = getpass.getpass('Enter admin password: ')
            password_confirm = getpass.getpass('Confirm admin password: ')
            if password == password_confirm:
                return password
            else:
                self.stdout.write(self.style.ERROR('Passwords do not match!'))
                return None
        except:
            return None

