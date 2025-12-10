"""
Script to test PostgreSQL database connection
Run this to verify your database is set up correctly
"""
import sys
import os

# Add the project to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferoute.settings')

import django
django.setup()

from django.db import connection
from django.conf import settings

def test_connection():
    """Test database connection"""
    print("=" * 50)
    print("Testing PostgreSQL Database Connection")
    print("=" * 50)
    
    # Display connection settings (without password)
    db_settings = settings.DATABASES['default']
    print(f"\nDatabase Configuration:")
    print(f"  Engine: {db_settings['ENGINE']}")
    print(f"  Name: {db_settings['NAME']}")
    print(f"  User: {db_settings['USER']}")
    print(f"  Host: {db_settings['HOST']}")
    print(f"  Port: {db_settings['PORT']}")
    print(f"  Password: {'*' * len(db_settings.get('PASSWORD', ''))}")
    
    print("\nAttempting to connect...")
    
    try:
        # Try to connect
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"\n✓ SUCCESS! Connected to PostgreSQL")
            print(f"  PostgreSQL Version: {version[0]}")
            
            # Check if database exists
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"  Current Database: {db_name}")
            
            # Test if we can create tables (check permissions)
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0]
            print(f"  Current User: {user}")
            
            print("\n✓ Database connection is working correctly!")
            return True
            
    except Exception as e:
        print(f"\n✗ ERROR: Failed to connect to database")
        print(f"  Error: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is installed and running")
        print("  2. Verify database name, user, and password in saferoute/settings.py")
        print("  3. Check if the database exists:")
        print("     - Open pgAdmin or use psql")
        print("     - Run: SELECT datname FROM pg_database;")
        print("  4. If database doesn't exist, create it:")
        print("     CREATE DATABASE saferoute_db;")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

