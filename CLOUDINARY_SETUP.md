# Cloudinary Setup Guide for SafeRoute

This guide will help you set up Cloudinary for image storage in your Django application.

## Step 1: Create a Cloudinary Account

1. Go to https://cloudinary.com/users/register/free
2. Sign up for a free account (includes 25GB storage and 25GB bandwidth)
3. Verify your email address

## Step 2: Get Your Cloudinary Credentials

1. After logging in, go to your **Dashboard**
2. You'll see your **Cloudinary credentials**:
   - **Cloud Name** (e.g., `dxyz1234`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)

3. **Copy these credentials** - you'll need them in the next step

## Step 3: Configure Environment Variables

### For Local Development

Create a `.env` file in your project root (if you don't have one):

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Note:** Make sure `.env` is in your `.gitignore` file (it should already be there).

### For Render Deployment

1. Go to your **Render Dashboard** → Your **Web Service**
2. Click on **"Environment"** tab
3. Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `CLOUDINARY_CLOUD_NAME` | `your_cloud_name` | Your Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | `your_api_key` | Your Cloudinary API key |
| `CLOUDINARY_API_SECRET` | `your_api_secret` | Your Cloudinary API secret |

4. Click **"Save Changes"**
5. Render will automatically redeploy your service

## Step 4: Install Dependencies

The required packages are already in `requirements.txt`. Install them:

```bash
pip install -r requirements.txt
```

Or if deploying to Render, the build script will install them automatically.

## Step 5: Run Migrations (If Needed)

If you've updated the models, create and run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Test the Setup

1. **Start your Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Upload an image:**
   - Go to `/admin/` and login
   - Create or edit an Incident Report
   - Upload an image
   - The image should now be stored in Cloudinary

3. **Verify in Cloudinary Dashboard:**
   - Go to https://cloudinary.com/console
   - Click on **"Media Library"**
   - You should see your uploaded images

## What's Configured

### Models Using Cloudinary:
- ✅ `IncidentImage.image` - Incident report images
- ✅ `IncidentVideo.video` - Video files
- ✅ `IncidentAudio.audio` - Audio files
- ✅ `CustomUser.profile_picture` - User profile pictures
- ✅ `CustomUser.id_document` - User ID documents

### Admin Features:
- ✅ Image previews in Django admin
- ✅ Thumbnail display in list views
- ✅ Full image preview in detail views
- ✅ Multiple image preview for reports

## Benefits of Cloudinary

1. **Automatic Image Optimization**: Images are automatically optimized for web
2. **CDN Delivery**: Fast global content delivery
3. **Transformations**: On-the-fly image transformations (resize, crop, etc.)
4. **No Local Storage**: No need to manage local file storage
5. **Scalable**: Handles high traffic and large files
6. **Free Tier**: 25GB storage and 25GB bandwidth per month

## Image URLs

Images stored in Cloudinary will have URLs like:
```
https://res.cloudinary.com/your_cloud_name/image/upload/v1234567890/incident_images/image.jpg
```

These URLs are automatically generated and stored in your database.

## Troubleshooting

### Images not uploading?

1. **Check environment variables:**
   - Verify all three Cloudinary credentials are set
   - Make sure there are no extra spaces or quotes

2. **Check Cloudinary dashboard:**
   - Go to https://cloudinary.com/console
   - Check if images are appearing in Media Library

3. **Check Django logs:**
   - Look for Cloudinary-related errors
   - Verify the storage backend is being used

### Images not displaying in admin?

1. **Clear browser cache**
2. **Check image URLs** - they should point to `res.cloudinary.com`
3. **Verify CLOUDINARY_CLOUD_NAME** is set correctly

### Fallback to Local Storage

If Cloudinary credentials are not set, the app will automatically fall back to local file storage. This is useful for:
- Development without Cloudinary account
- Testing locally
- Emergency fallback

## Security Best Practices

1. **Never commit credentials** to Git
2. **Use environment variables** for all credentials
3. **Rotate API secrets** periodically
4. **Use signed URLs** for private images (if needed)
5. **Set up Cloudinary upload presets** for better security

## Advanced Configuration

### Image Transformations

You can add transformations to image URLs. For example, in templates:

```django
<img src="{{ image.image.url }}" alt="Image">
```

Or with transformations:
```django
{% load cloudinary %}
{% cloudinary image.image.url width=300 height=300 crop="fill" %}
```

### Upload Presets

Create upload presets in Cloudinary dashboard for:
- Automatic image optimization
- Format conversion
- Size limits
- Security settings

## Support

- Cloudinary Documentation: https://cloudinary.com/documentation
- Django Cloudinary Storage: https://github.com/klis87/django-cloudinary-storage
- Cloudinary Support: https://support.cloudinary.com

---

**Your images are now stored in Cloudinary!** 🎉

