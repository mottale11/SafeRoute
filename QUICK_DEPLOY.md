# Quick Deployment Guide - Render

## 🚀 Fast Track Deployment (5 Minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Database on Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `saferoute-db`
4. Click **"Create Database"**
5. **Copy the Internal Database URL** (looks like `postgresql://...`)

### Step 3: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `saferoute-web`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn saferoute.wsgi:application`
4. Add Environment Variables:
   - `DJANGO_SECRET_KEY`: Generate with:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DJANGO_DEBUG`: `0`
   - `DATABASE_URL`: Paste the Internal Database URL from Step 2
5. Click **"Create Web Service"**

### Step 4: Wait for Deployment
- Build takes 2-3 minutes
- Watch the logs for success

### Step 5: Create Admin User
1. Go to your service → **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```

### Step 6: Access Your App
- Your app URL: `https://saferoute-web.onrender.com`
- Admin panel: `https://saferoute-web.onrender.com/admin/`

## ✅ Done!

For detailed instructions, see `DEPLOYMENT.md`

