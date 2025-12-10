from django.contrib import admin
from .models import (
    IncidentReport, IncidentImage, IncidentVideo, 
    IncidentAudio, SavedZone, HelpfulReport, CommunityDiscussion, DiscussionReply
)


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'severity', 'user', 'location_name', 'incident_date', 'is_verified', 'created_at')
    list_filter = ('category', 'severity', 'is_verified', 'created_at')
    search_fields = ('title', 'description', 'location_name')
    readonly_fields = ('created_at', 'updated_at', 'helpful_count', 'abuse_reports')


@admin.register(IncidentImage)
class IncidentImageAdmin(admin.ModelAdmin):
    list_display = ('report', 'image_type', 'is_blurred', 'created_at')
    list_filter = ('image_type', 'is_blurred')


admin.site.register(IncidentVideo)
admin.site.register(IncidentAudio)
admin.site.register(SavedZone)
admin.site.register(HelpfulReport)
admin.site.register(CommunityDiscussion)
admin.site.register(DiscussionReply)

