from django.contrib.auth.models import AbstractUser
from django.db import models

# Try to import Cloudinary storage, fallback to default if not available
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
    CLOUDINARY_STORAGE_AVAILABLE = True
except ImportError:
    MediaCloudinaryStorage = None
    CLOUDINARY_STORAGE_AVAILABLE = False


class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    id_document = models.ImageField(
        upload_to='user_ids/',
        storage=MediaCloudinaryStorage() if CLOUDINARY_STORAGE_AVAILABLE else None,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        storage=MediaCloudinaryStorage() if CLOUDINARY_STORAGE_AVAILABLE else None,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

