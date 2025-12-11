# Render Deployment Checklist

Use this checklist to ensure everything is ready for deployment.

## Pre-Deployment Checklist

### Code Preparation
- [x] All code committed to Git
- [x] Code pushed to GitHub repository
- [x] `requirements.txt` includes all dependencies (including gunicorn)
- [x] `build.sh` script created and executable
- [x] `render.yaml` configuration file created (optional)
- [x] `.gitignore` properly configured

### Configuration Files
- [x] `settings.py` configured for production:
  - [x] `DEBUG` set via environment variable (defaults to False when `DJANGO_DEBUG=0`)
  - [x] `ALLOWED_HOSTS` includes Render domains
  - [x] `CSRF_TRUSTED_ORIGINS` configured
  - [x] `DATABASE_URL` support via `dj_database_url`
  - [x] WhiteNoise middleware configured for static files
  - [x] `STATIC_ROOT` and `STATIC_URL` configured
  - [x] Security settings enabled (SECURE cookies, etc.)

### Database
- [ ] PostgreSQL database created on Render
- [ ] Database connection string copied
- [ ] Database migrations tested locally

### Environment Variables
- [ ] `DJANGO_SECRET_KEY` generated (use command in QUICK_DEPLOY.md)
- [ ] `DJANGO_DEBUG` set to `0`
- [ ] `DATABASE_URL` set to Render database connection string
- [ ] `RENDER_EXTERNAL_HOSTNAME` (auto-set by Render)

## Deployment Steps

### Step 1: Create Database
- [ ] Logged into Render dashboard
- [ ] Created PostgreSQL database
- [ ] Noted database credentials
- [ ] Copied Internal Database URL

### Step 2: Create Web Service
- [ ] Connected GitHub repository
- [ ] Created web service
- [ ] Set build command: `./build.sh`
- [ ] Set start command: `gunicorn saferoute.wsgi:application`
- [ ] Added all required environment variables
- [ ] Selected appropriate plan (Free/Starter)

### Step 3: Deploy
- [ ] Service created successfully
- [ ] Build completed without errors
- [ ] Application started successfully
- [ ] Health check passing

### Step 4: Post-Deployment
- [ ] Application accessible via URL
- [ ] Static files loading correctly
- [ ] Database connection working
- [ ] Created superuser account
- [ ] Admin panel accessible
- [ ] Tested user registration
- [ ] Tested user login
- [ ] Tested main pages (home, heatmap, etc.)

## Testing Checklist

### Functionality Tests
- [ ] Home page loads
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard accessible (when logged in)
- [ ] Heatmap page loads
- [ ] Submit report form works
- [ ] Gallery page loads
- [ ] Static files (CSS, images) load
- [ ] Admin panel accessible

### Security Tests
- [ ] HTTPS enabled (automatic on Render)
- [ ] DEBUG mode disabled in production
- [ ] Secret key is secure (not default)
- [ ] CSRF protection working
- [ ] Admin panel requires authentication

## Troubleshooting

If something doesn't work, check:

1. **Build Logs**: Service → Logs tab
   - Look for errors during build
   - Check if migrations ran
   - Verify static files collected

2. **Runtime Logs**: Service → Logs tab
   - Check for application errors
   - Verify database connection
   - Look for import errors

3. **Environment Variables**: Service → Environment tab
   - Verify all variables are set
   - Check for typos
   - Ensure DATABASE_URL is Internal URL

4. **Database**: Database service → Info tab
   - Verify database is running
   - Check connection string format
   - Ensure migrations ran

## Common Issues

### Issue: Build fails
- **Check**: `requirements.txt` has all packages
- **Check**: `build.sh` is executable
- **Check**: Python version matches

### Issue: Application crashes
- **Check**: Environment variables are set
- **Check**: Database connection string
- **Check**: ALLOWED_HOSTS includes your domain

### Issue: Static files not loading
- **Check**: WhiteNoise middleware in MIDDLEWARE
- **Check**: collectstatic ran in build
- **Check**: STATIC_ROOT is set

### Issue: Database errors
- **Check**: DATABASE_URL is correct
- **Check**: Using Internal Database URL
- **Check**: Migrations ran successfully

## Next Steps After Deployment

- [ ] Set up custom domain (optional)
- [ ] Configure email backend (for password resets)
- [ ] Set up monitoring/error tracking
- [ ] Configure backups
- [ ] Set up CI/CD (already automatic with Render)
- [ ] Optimize performance
- [ ] Set up CDN for static files (optional)



