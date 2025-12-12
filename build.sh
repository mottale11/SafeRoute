#!/usr/bin/env bash
# Exit on error
set -o errexit

# Build script for Render deployment

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (continue even if some files are missing)
python manage.py collectstatic --noinput || echo "Warning: collectstatic had some issues, but continuing..."

# Run database migrations
python manage.py migrate --noinput

# Create superuser if ADMIN_PASSWORD is set and no superuser exists
# This allows creating admin without shell access (useful for free tier)
if [ -n "$ADMIN_PASSWORD" ]; then
    echo "Creating admin user..."
    python manage.py create_superuser_auto --noinput || echo "Admin user creation skipped (may already exist)"
else
    echo "⚠️  ADMIN_PASSWORD not set. Skipping admin user creation."
    echo "   To create admin user, set ADMIN_PASSWORD environment variable in Render."
fi

