from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'email', 'is_verified_badge', 'is_staff_badge', 'is_superuser_badge', 'profile_picture_preview', 'report_count', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'date_joined', 'is_active')
    readonly_fields = ('profile_picture_preview', 'id_document_preview', 'date_joined', 'last_login', 'report_count')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    date_hierarchy = 'date_joined'
    list_per_page = 25
    
    def full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else '-'
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'
    
    def is_verified_badge(self, obj):
        if obj.is_verified:
            return format_html('<span class="badge badge-success">✓ Verified</span>')
        return format_html('<span class="badge badge-warning">Unverified</span>')
    is_verified_badge.short_description = 'Verification'
    is_verified_badge.admin_order_field = 'is_verified'
    
    def is_staff_badge(self, obj):
        if obj.is_staff:
            return format_html('<span class="badge badge-info">Staff</span>')
        return format_html('<span class="badge badge-secondary">User</span>')
    is_staff_badge.short_description = 'Role'
    is_staff_badge.admin_order_field = 'is_staff'
    
    def is_superuser_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span class="badge badge-danger">Admin</span>')
        return ''
    is_superuser_badge.short_description = 'Admin'
    is_superuser_badge.admin_order_field = 'is_superuser'
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #999;">No picture</span>')
    profile_picture_preview.short_description = 'Avatar'
    
    def report_count(self, obj):
        count = obj.incidentreport_set.count()
        if count > 0:
            url = reverse('admin:reports_incidentreport_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}" class="badge badge-primary">{}</a>', url, count)
        return format_html('<span class="badge badge-secondary">0</span>')
    report_count.short_description = 'Reports'
    
    def id_document_preview(self, obj):
        if obj.id_document:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.id_document.url
            )
        return format_html('<span style="color: #999;">No document uploaded</span>')
    id_document_preview.short_description = 'ID Document Preview'
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'is_verified', 'profile_picture', 'profile_picture_preview', 'id_document', 'id_document_preview')
        }),
        ('Activity', {
            'fields': ('report_count',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} user(s) verified.')
    verify_users.short_description = 'Verify selected users'
    
    def unverify_users(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} user(s) unverified.')
    unverify_users.short_description = 'Unverify selected users'

