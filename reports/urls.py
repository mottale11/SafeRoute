from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('submit/', views.submit_report_view, name='submit_report'),
    path('heatmap/', views.heatmap_view, name='heatmap'),
    path('reports/<int:report_id>/', views.report_detail_view, name='report_detail'),
    path('reports/<int:report_id>/helpful/', views.mark_helpful_view, name='mark_helpful'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('safety-tips/', views.safety_tips_view, name='safety_tips'),
    path('save-zone/', views.save_zone_view, name='save_zone'),
    path('community/', views.community_discussion_view, name='community'),
    path('community/new/', views.create_discussion_view, name='create_discussion'),
    path('community/<int:discussion_id>/', views.discussion_detail_view, name='discussion_detail'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms/', views.terms_view, name='terms'),
    path('about/', views.about_view, name='about'),
    path('api/incidents/', views.get_incidents_json, name='incidents_json'),
]

