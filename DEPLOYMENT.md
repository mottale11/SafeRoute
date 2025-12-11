# SafeRoute Deployment Guide for Render

This guide will walk you through deploying your SafeRoute Django application to Render, including both the database and web service.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Render account (sign up at https://render.com)

## Step 1: Prepare Your Repository

### 1.1 Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 1.2 Verify Required Files

Make sure these files are in your repository:
- ✅ `render.yaml` - Infrastructure as code configuration
- ✅ `build.sh` - Build script for deployment
- ✅ `requirements.txt` - Python dependencies (includes gunicorn)
- ✅ `manage.py` - Django management script

## Step 2: Create PostgreSQL Database on Render

### 2.1 Create Database Service

1. Log in to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure the database:
   - **Name**: `saferoute-db` (or any name you prefer)
   - **Database**: `saferoute_db`
   - **User**: `saferoute_user` (or leave default)
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (or latest)
   - **Plan**: 
     - **Free** for testing (limited to 90 days)
     - **Starter** ($7/month) for production
4. Click **"Create Database"**
5. **Wait for the database to be created** (takes 1-2 minutes)
6. **Copy the Internal Database URL** - you'll need this later
   - It looks like: `postgresql://user:password@host:port/database`

### 2.2 Note Database Credentials

From the database dashboard, note:
- **Host**: Database hostname
- **Port**: Usually 5432
- **Database**: Database name
- **User**: Database username
- **Password**: Database password (click "Show" to reveal)

## Step 3: Create Web Service on Render

### 3.1 Connect Your Repository

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select your repository: `SafeRoute` (or your repo name)
4. Click **"Connect"**

### 3.2 Configure Web Service

Fill in the configuration:

**Basic Settings:**
- **Name**: `saferoute-web` (or any name)
- **Region**: Same region as your database
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or `.` if needed)
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn saferoute.wsgi:application`

**Environment Variables:**
Click **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `DJANGO_SECRET_KEY` | `[Generate a secret key]` | See below for generation |
| `DJANGO_DEBUG` | `0` | Set to 0 for production |
| `DATABASE_URL` | `[From database service]` | Use Internal Database URL from Step 2.1 |
| `RENDER_EXTERNAL_HOSTNAME` | `[Auto-filled]` | Will be set automatically |

**Generate Django Secret Key:**
Run this in your terminal:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as `DJANGO_SECRET_KEY`.

**Advanced Settings:**
- **Instance Type**: 
  - **Free** for testing (spins down after inactivity)
  - **Starter** ($7/month) for production (always on)
- **Health Check Path**: `/`

### 3.3 Create Web Service

Click **"Create Web Service"**

Render will now:
1. Clone your repository
2. Run the build script (`build.sh`)
3. Start your application with gunicorn

## Step 4: Configure Static Files (Already Set Up)

Your project is already configured with WhiteNoise for static file serving. The `build.sh` script runs `collectstatic` automatically.

## Step 5: Set Up Media Files Storage

**Important**: Render's filesystem is ephemeral. Uploaded files will be lost on redeploy.

### Option A: Use Render Disk (Temporary Solution)
- Free tier includes 1GB disk
- Files persist between deploys but not between service recreations

### Option B: Use Cloud Storage (Recommended for Production)
Consider using:
- **AWS S3** with `django-storages`
- **Cloudinary** for images
- **Google Cloud Storage**

For now, the current setup will work for testing.

## Step 6: Verify Deployment

### 6.1 Check Build Logs

1. In your web service dashboard, go to **"Logs"** tab
2. Watch for:
   - ✅ "Build successful"
   - ✅ "Collecting static files..."
   - ✅ "Running migrations..."
   - ✅ "Starting gunicorn..."

### 6.2 Test Your Application

1. Click on your service URL (e.g., `https://saferoute-web.onrender.com`)
2. Test these pages:
   - Home page: `/`
   - Registration: `/accounts/register/`
   - Login: `/accounts/login/`
   - Heatmap: `/heatmap/`

### 6.3 Create Superuser (Admin Access)

**Note:** Free tier doesn't include Shell access. Use one of these methods:

**Method 1: Environment Variables (Recommended)**
1. In Render dashboard, go to your web service
2. Click **"Environment"** tab
3. Add these environment variables:
   - `ADMIN_USERNAME`: `admin` (or your preferred username)
   - `ADMIN_EMAIL`: `admin@yourdomain.com`
   - `ADMIN_PASSWORD`: `YourSecurePassword123!` (use a strong password)
4. Redeploy your service (or it will auto-redeploy)
5. Admin user will be created automatically during build
6. Access admin at: `https://your-app.onrender.com/admin/`

**Method 2: Management Command**
If you have Shell access (paid tier), run:
```bash
python manage.py createsuperuser
```

For detailed instructions on all methods, see `CREATE_ADMIN_GUIDE.md`

## Step 7: Environment Variables Reference

Here's a complete list of environment variables you can set:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | ✅ Yes | - | Django secret key for security |
| `DJANGO_DEBUG` | ✅ Yes | `0` | Set to `0` for production |
| `DATABASE_URL` | ✅ Yes | - | PostgreSQL connection string |
| `RENDER_EXTERNAL_HOSTNAME` | Auto | - | Your app's hostname (auto-set) |
| `PYTHON_VERSION` | No | `3.11.0` | Python version |
| `ADMIN_USERNAME` | No | `admin` | Admin username (for auto-creation, free tier) |
| `ADMIN_EMAIL` | No | `admin@saferoute.com` | Admin email (for auto-creation, free tier) |
| `ADMIN_PASSWORD` | No | - | Admin password (for auto-creation, free tier method) |

## Step 8: Using render.yaml (Alternative Method)

Instead of manually creating services, you can use the `render.yaml` file:

1. In Render dashboard, click **"New +"** → **"Blueprint"**
2. Connect your repository
3. Render will automatically detect `render.yaml`
4. Review the services and click **"Apply"**

This creates both the database and web service automatically.

## Troubleshooting

### Build Fails

**Error**: "Module not found"
- **Solution**: Check `requirements.txt` includes all dependencies

**Error**: "Collectstatic failed"
- **Solution**: Ensure `STATIC_ROOT` is set in `settings.py` (already configured)

**Error**: "Migration failed"
- **Solution**: Check database connection string is correct

### Application Crashes

**Error**: "DisallowedHost"
- **Solution**: Ensure `ALLOWED_HOSTS` includes your Render domain (already configured)

**Error**: "Database connection failed"
- **Solution**: 
  - Verify `DATABASE_URL` is correct
  - Use **Internal Database URL** (not External)
  - Check database is running

**Error**: "Static files not loading"
- **Solution**: 
  - Verify WhiteNoise middleware is in `MIDDLEWARE` (already configured)
  - Check `collectstatic` ran successfully in build logs

### Database Issues

**Error**: "Relation does not exist"
- **Solution**: Run migrations manually in Shell:
  ```bash
  python manage.py migrate
  ```

**Error**: "Permission denied"
- **Solution**: Check database user has proper permissions

## Step 9: Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] Static files (CSS, images) load correctly
- [ ] Database connection works
- [ ] User registration works
- [ ] User login works
- [ ] Admin panel accessible
- [ ] File uploads work (if implemented)
- [ ] All pages load correctly
- [ ] HTTPS is enabled (automatic on Render)

## Step 10: Monitoring and Maintenance

### View Logs
- Go to your service → **"Logs"** tab
- Real-time logs help debug issues

### Update Application
1. Push changes to GitHub
2. Render automatically redeploys
3. Monitor build logs

### Database Backups
- Free tier: Manual backups only
- Paid tiers: Automatic daily backups
- Export database: Use `pg_dump` in Shell

## Security Checklist

- [x] `DEBUG = False` in production (via `DJANGO_DEBUG=0`)
- [x] Strong `SECRET_KEY` set
- [x] `ALLOWED_HOSTS` configured
- [x] `CSRF_TRUSTED_ORIGINS` set
- [x] HTTPS enabled (automatic on Render)
- [ ] Regular security updates
- [ ] Database credentials secured

## Cost Estimation

**Free Tier:**
- Web Service: Free (spins down after 15 min inactivity)
- Database: Free (90 days, then $7/month)
- Total: $0 for 90 days, then $7/month

**Starter Tier (Recommended for Production):**
- Web Service: $7/month (always on)
- Database: $7/month
- Total: $14/month

## Next Steps

1. **Set up custom domain** (optional):
   - Go to service settings
   - Add custom domain
   - Update DNS records

2. **Set up monitoring**:
   - Use Render's built-in monitoring
   - Set up error tracking (Sentry, etc.)

3. **Optimize performance**:
   - Enable caching
   - Optimize database queries
   - Use CDN for static files

4. **Set up CI/CD**:
   - Render auto-deploys on git push
   - Add tests to your workflow



## Quick Reference Commands

**Access Shell:**
- Render Dashboard → Your Service → Shell tab

**Run Django commands:**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```




