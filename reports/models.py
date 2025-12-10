from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class IncidentReport(models.Model):
    """Main incident report model"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ]
    
    CATEGORY_CHOICES = [
        ('theft', 'Theft'),
        ('harassment', 'Harassment'),
        ('assault', 'Assault'),
        ('road_danger', 'Road Danger'),
        ('fraud', 'Fraud/Scam'),
        ('violence', 'Violence'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_name = models.CharField(max_length=200, blank=True)
    incident_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    abuse_reports = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"


class IncidentImage(models.Model):
    """Images associated with incidents"""
    IMAGE_TYPE_CHOICES = [
        ('suspect', 'Suspect/Offender Photo'),
        ('location', 'Location Photo'),
        ('evidence', 'Other Evidence'),
    ]
    
    report = models.ForeignKey(IncidentReport, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='incident_images/')
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    is_blurred = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_image_type_display()} - {self.report.title}"


class IncidentVideo(models.Model):
    """Videos associated with incidents"""
    report = models.ForeignKey(IncidentReport, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='incident_videos/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IncidentAudio(models.Model):
    """Audio recordings associated with incidents"""
    report = models.ForeignKey(IncidentReport, related_name='audio_files', on_delete=models.CASCADE)
    audio = models.FileField(upload_to='incident_audio/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedZone(models.Model):
    """User-saved risk zones"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # in km
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class HelpfulReport(models.Model):
    """Users marking reports as helpful"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'report']
    
    def __str__(self):
        return f"{self.user.username} marked {self.report.title} as helpful"


class CommunityDiscussion(models.Model):
    """Community discussion posts"""
    CATEGORY_CHOICES = [
        ('areas_to_avoid', 'Areas to Avoid'),
        ('suspicious_activities', 'Suspicious Activities'),
        ('lost_found', 'Lost & Found'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class DiscussionReply(models.Model):
    """Replies to community discussion posts"""
    discussion = models.ForeignKey(CommunityDiscussion, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.user.username}"

