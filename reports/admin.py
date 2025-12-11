from django.contrib import admin
from django.utils.html import format_html
from .models import (
    IncidentReport, IncidentImage, IncidentVideo, 
    IncidentAudio, SavedZone, HelpfulReport, CommunityDiscussion, DiscussionReply
)


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'severity', 'user', 'location_name', 'incident_date', 'is_verified', 'created_at')
    list_filter = ('category', 'severity', 'is_verified', 'created_at')
    search_fields = ('title', 'description', 'location_name')
    readonly_fields = ('created_at', 'updated_at', 'helpful_count', 'abuse_reports', 'images_preview')
    filter_horizontal = ()
    
    def images_preview(self, obj):
        images = obj.images.all()[:5]  # Show first 5 images
        if images:
            html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
            for img in images:
                html += format_html(
                    '<div style="text-align: center;"><img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 5px; margin-bottom: 5px;" /><br><small>{}</small></div>',
                    img.image.url,
                    img.get_image_type_display()
                )
            html += '</div>'
            return format_html(html)
        return "No images"
    images_preview.short_description = 'Report Images'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'category', 'severity', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'location_name', 'incident_date')
        }),
        ('Status', {
            'fields': ('is_verified', 'helpful_count', 'abuse_reports')
        }),
        ('Images', {
            'fields': ('images_preview',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(IncidentImage)
class IncidentImageAdmin(admin.ModelAdmin):
    list_display = ('report', 'image_type', 'is_blurred', 'image_preview', 'created_at')
    list_filter = ('image_type', 'is_blurred')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 5px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        (None, {
            'fields': ('report', 'image', 'image_preview', 'image_type', 'is_blurred', 'description')
        }),
    )


admin.site.register(IncidentVideo)
admin.site.register(IncidentAudio)
admin.site.register(SavedZone)
admin.site.register(HelpfulReport)
admin.site.register(CommunityDiscussion)
admin.site.register(DiscussionReply)

