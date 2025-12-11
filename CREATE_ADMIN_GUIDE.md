# Creating Admin User on Render (Free Tier - No Shell Access)

Since Render's free tier doesn't include Shell access, here are **3 alternative methods** to create a superuser/admin account:

## Method 1: Environment Variables (Recommended) ⭐

This is the **easiest and most secure** method. The admin user will be created automatically during deployment.

### Step 1: Add Environment Variables in Render

1. Go to your **Web Service** dashboard on Render
2. Click on **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add these variables:

| Key | Value | Description |
|-----|-------|-------------|
| `ADMIN_USERNAME` | `admin` | Your admin username (or choose your own) |
| `ADMIN_EMAIL` | `admin@yourdomain.com` | Admin email address |
| `ADMIN_PASSWORD` | `YourSecurePassword123!` | Admin password (use a strong password!) |

### Step 2: Redeploy Your Service

1. After adding the environment variables, Render will automatically redeploy
2. Or manually trigger a redeploy: Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Watch the build logs - you should see: `✅ Superuser "admin" created successfully!`

### Step 3: Access Admin Panel

1. Go to: `https://your-app.onrender.com/admin/`
2. Login with:
   - Username: `admin` (or whatever you set)
   - Password: Your `ADMIN_PASSWORD` value

**✅ Done!** This method works automatically and is the most secure.

---

## Method 2: Management Command via Build Script

The `build.sh` script already includes automatic admin creation. Just set the environment variables as in Method 1, and it will work automatically.

If you want to customize it further, you can modify `build.sh`:

```bash
# Create superuser with custom settings
python manage.py create_superuser_auto \
    --username admin \
    --email admin@example.com \
    --password "$ADMIN_PASSWORD" \
    --noinput
```

---

## Method 3: Temporary Admin Creation View (Less Secure)

If you need to create an admin user after deployment without redeploying, you can temporarily add a view that creates an admin user.

### ⚠️ Warning: This method is less secure. Remove it after creating admin!

### Step 1: Add Temporary View

Create a file `accounts/views_admin.py`:

```python
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import os

User = get_user_model()

@csrf_exempt
def create_admin_view(request):
    """Temporary view to create admin user - REMOVE AFTER USE!"""
    # Only allow if ADMIN_CREATE_TOKEN is set and matches
    token = request.GET.get('token') or request.POST.get('token')
    expected_token = os.environ.get('ADMIN_CREATE_TOKEN')
    
    if not expected_token or token != expected_token:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    username = request.POST.get('username', 'admin')
    email = request.POST.get('email', 'admin@saferoute.com')
    password = request.POST.get('password')
    
    if not password:
        return JsonResponse({'error': 'Password required'}, status=400)
    
    if User.objects.filter(is_superuser=True).exists():
        return JsonResponse({'message': 'Admin already exists'})
    
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        return JsonResponse({'message': f'Admin user "{username}" created successfully!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### Step 2: Add URL (Temporarily)

In `accounts/urls.py`, add:

```python
from .views_admin import create_admin_view

urlpatterns = [
    # ... existing patterns ...
    path('create-admin/', create_admin_view, name='create_admin'),  # REMOVE AFTER USE!
]
```

### Step 3: Set Security Token

In Render dashboard, add environment variable:
- `ADMIN_CREATE_TOKEN`: A random secret token (e.g., generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Step 4: Create Admin

Visit (replace `YOUR_TOKEN` with your token):
```
https://your-app.onrender.com/accounts/create-admin/?token=YOUR_TOKEN
```

Or use curl:
```bash
curl -X POST https://your-app.onrender.com/accounts/create-admin/ \
  -d "token=YOUR_TOKEN&username=admin&email=admin@example.com&password=YourPassword123!"
```

### Step 5: Remove the View and URL

**⚠️ IMPORTANT:** After creating admin, remove:
1. The `create_admin_view` from `accounts/views_admin.py`
2. The URL pattern from `accounts/urls.py`
3. The `ADMIN_CREATE_TOKEN` environment variable
4. Commit and push changes

---

## Method 4: Use Django Admin Directly (If You Can Register)

If user registration is open, you can:

1. Register a regular user account
2. Manually promote it to superuser via database (if you have access)
3. Or use Method 1 to create admin, then promote the user via admin panel

---

## Recommended Approach

**Use Method 1 (Environment Variables)** because:
- ✅ Most secure
- ✅ Automatic during deployment
- ✅ No code changes needed
- ✅ Works with free tier
- ✅ No manual intervention required

## Troubleshooting

### Admin user not created?

1. **Check build logs** in Render dashboard:
   - Look for: `Creating admin user...`
   - Check for errors

2. **Verify environment variables**:
   - `ADMIN_PASSWORD` must be set
   - `ADMIN_USERNAME` is optional (defaults to 'admin')
   - `ADMIN_EMAIL` is optional (defaults to 'admin@saferoute.com')

3. **Check if admin already exists**:
   - The script skips creation if a superuser already exists
   - Try logging in with your credentials

4. **Redeploy**:
   - After adding environment variables, trigger a manual redeploy

### Can't login to admin?

1. **Verify credentials**: Use the exact values from environment variables
2. **Check admin URL**: Should be `/admin/`
3. **Verify user exists**: Check if superuser was created in build logs
4. **Reset password**: If needed, use Method 3 temporarily to reset

---

## Security Best Practices

1. **Use strong password** for `ADMIN_PASSWORD`
2. **Change password** after first login
3. **Don't commit** admin credentials to Git
4. **Remove temporary views** after use (Method 3)
5. **Use environment variables** (Method 1) instead of hardcoding

---

## Quick Reference

**To create admin via environment variables:**

1. Render Dashboard → Your Service → Environment
2. Add: `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
3. Redeploy
4. Login at: `https://your-app.onrender.com/admin/`

**That's it!** 🎉

