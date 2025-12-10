# SafeRoute Setup Guide

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Database Setup

You need to create a PostgreSQL database before running the Django application. Here are several methods:

#### Method 1: Using psql (Command Line)

1. **Open Command Prompt or PowerShell** (Windows) or Terminal (Mac/Linux)

2. **Connect to PostgreSQL** (you may need to use the postgres superuser):
   ```bash
   psql -U postgres
   ```
   Or if you need to specify a host:
   ```bash
   psql -U postgres -h localhost
   ```
   
   You'll be prompted for the postgres user password.

3. **Once connected, run these SQL commands**:
   ```sql
   CREATE DATABASE saferoute_db;
   CREATE USER saferoute_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE saferoute_db TO saferoute_user;
   ALTER USER saferoute_user CREATEDB;
   \q
   ```
   (Replace `your_secure_password` with a strong password)

#### Method 2: Using pgAdmin (GUI Tool)

1. **Download and install pgAdmin** from https://www.pgadmin.org/download/

2. **Open pgAdmin** and connect to your PostgreSQL server

3. **Right-click on "Databases"** → **Create** → **Database**

4. **Enter database name**: `saferoute_db`

5. **Click "Save"**

6. **To create a user**: 
   - Right-click on "Login/Group Roles" → **Create** → **Login/Group Role**
   - Name: `saferoute_user`
   - Go to "Definition" tab → Enter password
   - Go to "Privileges" tab → Enable "Can login?" and "Create databases?"
   - Click "Save"

#### Method 3: Using Command Line (One-liner)

If PostgreSQL is in your PATH, you can create the database directly:

**Windows (PowerShell):**
```powershell
psql -U postgres -c "CREATE DATABASE saferoute_db;"
psql -U postgres -c "CREATE USER saferoute_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE saferoute_db TO saferoute_user;"
```

**Mac/Linux:**
```bash
sudo -u postgres psql -c "CREATE DATABASE saferoute_db;"
sudo -u postgres psql -c "CREATE USER saferoute_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE saferoute_db TO saferoute_user;"
```

#### Verify Database Creation

To verify the database was created:
```bash
psql -U postgres -l
```
You should see `saferoute_db` in the list.

### 2. Update Database Settings

Edit `saferoute/settings.py` and update the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saferoute_db',
        'USER': 'saferoute_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Collect Static Files (for production)

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Testing the Application

1. **Access the landing page**: `http://127.0.0.1:8000`
2. **Register a new account**: Click "Register" and fill in the form
3. **Login**: Use your credentials to log in
4. **Submit a test report**: Go to "Submit Report" and create a test incident
5. **View the heatmap**: Navigate to "Heatmap" to see reported incidents
6. **Access admin panel**: Go to `http://127.0.0.1:8000/admin` and verify reports

## Admin Panel Features

- View and manage all incident reports
- Verify reports to make them public
- Manage users and their verification status
- View uploaded images and media
- Monitor helpful reports and abuse reports

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running
- Verify database credentials in settings.py
- Check that the database exists

### Static Files Not Loading

- Run `python manage.py collectstatic`
- Ensure `STATIC_URL` and `STATIC_ROOT` are correctly configured
- Check that static files are in the `static/` directory

### Media Files Not Uploading

- Ensure `MEDIA_ROOT` directory exists and is writable
- Check `MEDIA_URL` configuration
- Verify file permissions on the media directory

### Map Not Displaying

- Check internet connection (Leaflet.js loads from CDN)
- Verify JavaScript console for errors
- Ensure coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)

## Production Deployment Notes

Before deploying to production:

1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS` with your domain
4. Configure proper database credentials
5. Set up proper static file serving
6. Configure media file storage (consider using cloud storage)
7. Set up SSL/HTTPS
8. Configure proper logging
9. Set up backup procedures for the database
10. Review security settings and CSRF configuration

## Environment Variables (Recommended)

Create a `.env` file for sensitive settings:

```
SECRET_KEY=your-secret-key-here
DB_NAME=saferoute_db
DB_USER=saferoute_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Then use `python-decouple` or `django-environ` to load these values.

