from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    IncidentReport, IncidentImage, IncidentVideo, 
    IncidentAudio, SavedZone, HelpfulReport, CommunityDiscussion, DiscussionReply
)


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_badge', 'severity_badge', 'user_link', 'location_name', 'incident_date', 'is_verified_badge', 'created_at', 'actions_column')
    list_filter = ('category', 'severity', 'is_verified', 'created_at', 'incident_date')
    search_fields = ('title', 'description', 'location_name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'helpful_count', 'abuse_reports', 'images_preview', 'location_map_link')
    filter_horizontal = ()
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_max_show_all = 100
    
    def category_badge(self, obj):
        colors = {
            'theft': 'warning',
            'assault': 'danger',
            'harassment': 'info',
            'road_danger': 'warning',
            'fraud': 'danger',
            'violence': 'danger',
            'other': 'dark'
        }
        color = colors.get(obj.category, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_category_display()
        )
    category_badge.short_description = 'Category'
    category_badge.admin_order_field = 'category'
    
    def severity_badge(self, obj):
        colors = {
            'low': 'success',
            'moderate': 'warning',
            'high': 'danger'
        }
        color = colors.get(obj.severity, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_severity_display().upper()
        )
    severity_badge.short_description = 'Severity'
    severity_badge.admin_order_field = 'severity'
    
    def is_verified_badge(self, obj):
        if obj.is_verified:
            return format_html('<span class="badge badge-success">✓ Verified</span>')
        return format_html('<span class="badge badge-warning">Pending</span>')
    is_verified_badge.short_description = 'Status'
    is_verified_badge.admin_order_field = 'is_verified'
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_customuser_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
    
    def location_map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">View on Google Maps</a>', url)
        return 'No coordinates'
    location_map_link.short_description = 'Location'
    
    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>',
            reverse('admin:reports_incidentreport_change', args=[obj.pk])
        )
    actions_column.short_description = 'Actions'
    
    def images_preview(self, obj):
        images = obj.images.all()[:5]  # Show first 5 images
        if images:
            html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
            for img in images:
                html += format_html(
                    '<div style="text-align: center;"><img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 5px; margin-bottom: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" /><br><small>{}</small></div>',
                    img.image.url,
                    img.get_image_type_display()
                )
            html += '</div>'
            return format_html(html)
        return format_html('<span style="color: #999;">No images</span>')
    images_preview.short_description = 'Report Images'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'category', 'severity', 'description'),
            'classes': ('wide',)
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'location_name', 'location_map_link', 'incident_date'),
            'classes': ('wide',)
        }),
        ('Status & Engagement', {
            'fields': ('is_verified', 'helpful_count', 'abuse_reports'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('images_preview',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} report(s) marked as verified.')
    mark_as_verified.short_description = 'Mark selected reports as verified'
    
    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} report(s) marked as unverified.')
    mark_as_unverified.short_description = 'Mark selected reports as unverified'


@admin.register(IncidentImage)
class IncidentImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_link', 'image_type_badge', 'is_blurred_badge', 'image_preview', 'created_at')
    list_filter = ('image_type', 'is_blurred', 'created_at')
    search_fields = ('report__title', 'description')
    readonly_fields = ('image_preview', 'created_at')
    date_hierarchy = 'created_at'
    
    def report_link(self, obj):
        if obj.report:
            url = reverse('admin:reports_incidentreport_change', args=[obj.report.pk])
            return format_html('<a href="{}">{}</a>', url, obj.report.title[:50])
        return '-'
    report_link.short_description = 'Report'
    report_link.admin_order_field = 'report__title'
    
    def image_type_badge(self, obj):
        return format_html(
            '<span class="badge badge-info">{}</span>',
            obj.get_image_type_display()
        )
    image_type_badge.short_description = 'Type'
    image_type_badge.admin_order_field = 'image_type'
    
    def is_blurred_badge(self, obj):
        if obj.is_blurred:
            return format_html('<span class="badge badge-warning">Blurred</span>')
        return format_html('<span class="badge badge-success">Clear</span>')
    is_blurred_badge.short_description = 'Blur Status'
    is_blurred_badge.admin_order_field = 'is_blurred'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Image Information', {
            'fields': ('report', 'image', 'image_preview', 'image_type', 'is_blurred', 'description'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(IncidentVideo)
class IncidentVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_link', 'video_type', 'is_blurred_badge', 'created_at')
    list_filter = ('video_type', 'is_blurred', 'created_at')
    search_fields = ('report__title', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def report_link(self, obj):
        if obj.report:
            url = reverse('admin:reports_incidentreport_change', args=[obj.report.pk])
            return format_html('<a href="{}">{}</a>', url, obj.report.title[:50])
        return '-'
    report_link.short_description = 'Report'
    
    def is_blurred_badge(self, obj):
        if obj.is_blurred:
            return format_html('<span class="badge badge-warning">Blurred</span>')
        return format_html('<span class="badge badge-success">Clear</span>')
    is_blurred_badge.short_description = 'Blur Status'


@admin.register(IncidentAudio)
class IncidentAudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_link', 'audio_type', 'duration', 'created_at')
    list_filter = ('audio_type', 'created_at')
    search_fields = ('report__title', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def report_link(self, obj):
        if obj.report:
            url = reverse('admin:reports_incidentreport_change', args=[obj.report.pk])
            return format_html('<a href="{}">{}</a>', url, obj.report.title[:50])
        return '-'
    report_link.short_description = 'Report'


@admin.register(SavedZone)
class SavedZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'name', 'latitude', 'longitude', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'location_map_link')
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_customuser_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def location_map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">View on Google Maps</a>', url)
        return 'No coordinates'
    location_map_link.short_description = 'Location'


@admin.register(HelpfulReport)
class HelpfulReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'report_link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'report__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_customuser_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def report_link(self, obj):
        if obj.report:
            url = reverse('admin:reports_incidentreport_change', args=[obj.report.pk])
            return format_html('<a href="{}">{}</a>', url, obj.report.title[:50])
        return '-'
    report_link.short_description = 'Report'


@admin.register(CommunityDiscussion)
class CommunityDiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_link', 'report_link', 'reply_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'user__username', 'report__title')
    readonly_fields = ('created_at', 'updated_at', 'reply_count')
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_customuser_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def report_link(self, obj):
        if obj.report:
            url = reverse('admin:reports_incidentreport_change', args=[obj.report.pk])
            return format_html('<a href="{}">{}</a>', url, obj.report.title[:50])
        return '-'
    report_link.short_description = 'Report'
    
    def reply_count(self, obj):
        count = obj.replies.count()
        return format_html('<span class="badge badge-info">{}</span>', count)
    reply_count.short_description = 'Replies'
    reply_count.admin_order_field = 'replies__count'


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'discussion_link', 'user_link', 'preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'discussion__title')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def discussion_link(self, obj):
        if obj.discussion:
            url = reverse('admin:reports_communitydiscussion_change', args=[obj.discussion.pk])
            return format_html('<a href="{}">{}</a>', url, obj.discussion.title[:50])
        return '-'
    discussion_link.short_description = 'Discussion'
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_customuser_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def preview(self, obj):
        return format_html('<span>{}</span>', obj.content[:100] + '...' if len(obj.content) > 100 else obj.content)
    preview.short_description = 'Content Preview'

