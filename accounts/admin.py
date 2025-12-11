from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_verified', 'is_staff', 'profile_picture_preview', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    readonly_fields = ('profile_picture_preview', 'id_document_preview')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return "No picture"
    profile_picture_preview.short_description = 'Profile Picture'
    
    def id_document_preview(self, obj):
        if obj.id_document:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 5px;" />',
                obj.id_document.url
            )
        return "No document"
    id_document_preview.short_description = 'ID Document'
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'is_verified', 'profile_picture', 'profile_picture_preview', 'id_document', 'id_document_preview')
        }),
    )

