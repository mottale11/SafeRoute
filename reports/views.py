from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import IncidentReport, IncidentImage, SavedZone, HelpfulReport, CommunityDiscussion, DiscussionReply
from .forms import IncidentReportForm, IncidentImageForm, SavedZoneForm
from datetime import timedelta
import json


def home_view(request):
    """Landing page"""
    try:
        # Get recent incidents for display with images
        recent_incidents = IncidentReport.objects.filter(is_verified=True).select_related('user').prefetch_related('images').order_by('-created_at')[:6]
        
        # Calculate risk zones for mini-heatmap
        high_risk_count = IncidentReport.objects.filter(severity='high', is_verified=True).count()
        moderate_risk_count = IncidentReport.objects.filter(severity='moderate', is_verified=True).count()
        safe_zones_count = IncidentReport.objects.filter(severity='low', is_verified=True).count()
    except Exception as e:
        # If database tables don't exist yet, use empty defaults
        recent_incidents = []
        high_risk_count = 0
        moderate_risk_count = 0
        safe_zones_count = 0
    
    context = {
        'recent_incidents': recent_incidents,
        'high_risk_count': high_risk_count,
        'moderate_risk_count': moderate_risk_count,
        'safe_zones_count': safe_zones_count,
    }
    return render(request, 'reports/home.html', context)


@login_required
def dashboard_view(request):
    """User dashboard"""
    try:
        user = request.user
        user_reports = IncidentReport.objects.filter(user=user).order_by('-created_at')[:5]
        saved_zones = SavedZone.objects.filter(user=user)
        
        # Activity feed - recent incidents with images
        area_incidents = IncidentReport.objects.filter(is_verified=True).select_related('user').prefetch_related('images').order_by('-created_at')[:10]
        
        # Calculate helpful counts and comment counts for each incident
        for incident in area_incidents:
            incident.comment_count = 0  # Placeholder for future comment feature
    except Exception as e:
        # If database tables don't exist yet, use empty defaults
        user_reports = []
        saved_zones = []
        area_incidents = []
    
    context = {
        'user': request.user,
        'user_reports': user_reports,
        'saved_zones': saved_zones,
        'area_incidents': area_incidents,
    }
    return render(request, 'reports/dashboard.html', context)


@login_required
def submit_report_view(request):
    """Incident reporting page"""
    if request.method == 'POST':
        report_form = IncidentReportForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.save()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            for img in images:
                image_type = request.POST.get('image_type', 'evidence')
                IncidentImage.objects.create(
                    report=report,
                    image=img,
                    image_type=image_type,
                    is_blurred=True
                )
            
            messages.success(request, 'Incident report submitted successfully! It will be reviewed before being made public.')
            return redirect('reports:report_detail', report_id=report.id)
    else:
        report_form = IncidentReportForm()
    
    return render(request, 'reports/submit_report.html', {'form': report_form})


def heatmap_view(request):
    """Public safety heatmap page"""
    try:
        # Get filter parameters
        category = request.GET.get('category', '')
        severity = request.GET.get('severity', '')
        time_filter = request.GET.get('time', 'all')
        
        # Base queryset
        reports = IncidentReport.objects.filter(is_verified=True)
        
        # Apply filters
        if category:
            reports = reports.filter(category=category)
        if severity:
            reports = reports.filter(severity=severity)
        if time_filter == '24h':
            reports = reports.filter(created_at__gte=timezone.now() - timedelta(days=1))
        elif time_filter == 'week':
            reports = reports.filter(created_at__gte=timezone.now() - timedelta(days=7))
        elif time_filter == 'month':
            reports = reports.filter(created_at__gte=timezone.now() - timedelta(days=30))
        
        # Get user's saved zones (if authenticated) - for display in template
        user_saved_zones = []
        if request.user.is_authenticated:
            try:
                user_saved_zones = SavedZone.objects.filter(user=request.user)
            except:
                pass
        
        # Get saved zones for map (JSON)
        saved_zones_json = []
        if request.user.is_authenticated:
            try:
                user_zones = SavedZone.objects.filter(user=request.user)
                for zone in user_zones:
                    saved_zones_json.append({
                        'name': zone.name,
                        'latitude': float(zone.latitude),
                        'longitude': float(zone.longitude),
                        'radius': float(zone.radius),
                    })
            except:
                pass
        
        # Serialize for map
        incidents_data = []
        for report in reports:
            incidents_data.append({
                'id': report.id,
                'title': report.title,
                'category': report.get_category_display(),
                'severity': report.severity,
                'latitude': float(report.latitude),
                'longitude': float(report.longitude),
                'location_name': report.location_name or '',
                'incident_date': report.incident_date.isoformat(),
                'url': f'/reports/{report.id}/',
            })
    except Exception as e:
        # If database tables don't exist yet, use empty defaults
        incidents_data = []
        saved_zones_json = []
        user_saved_zones = []
        category = request.GET.get('category', '')
        severity = request.GET.get('severity', '')
        time_filter = request.GET.get('time', 'all')
    
    context = {
        'incidents': json.dumps(incidents_data),
        'saved_zones': json.dumps(saved_zones_json),
        'user_saved_zones': user_saved_zones,
        'selected_category': category,
        'selected_severity': severity,
        'selected_time': time_filter,
    }
    return render(request, 'reports/heatmap.html', context)


def report_detail_view(request, report_id):
    """Incident details page"""
    report = get_object_or_404(IncidentReport, id=report_id)
    images = report.images.all()
    is_helpful = False
    
    if request.user.is_authenticated:
        is_helpful = HelpfulReport.objects.filter(user=request.user, report=report).exists()
    
    context = {
        'report': report,
        'images': images,
        'is_helpful': is_helpful,
    }
    return render(request, 'reports/report_detail.html', context)


@login_required
def mark_helpful_view(request, report_id):
    """Mark a report as helpful"""
    report = get_object_or_404(IncidentReport, id=report_id)
    helpful, created = HelpfulReport.objects.get_or_create(user=request.user, report=report)
    
    if created:
        report.helpful_count += 1
        report.save()
        messages.success(request, 'Thank you for marking this report as helpful!')
    else:
        messages.info(request, 'You have already marked this report as helpful.')
    
    return redirect('reports:report_detail', report_id=report_id)


def gallery_view(request):
    """Suspects & Risk Locations Gallery"""
    try:
        image_type = request.GET.get('type', 'all')
        category = request.GET.get('category', '')
        
        images = IncidentImage.objects.filter(report__is_verified=True)
        
        if image_type == 'suspect':
            images = images.filter(image_type='suspect')
        elif image_type == 'location':
            images = images.filter(image_type='location')
        
        if category:
            images = images.filter(report__category=category)
        
        images = images.order_by('-created_at')
        
        # Pagination
        paginator = Paginator(images, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        # If database tables don't exist yet, use empty defaults
        from django.core.paginator import EmptyPage, PageNotAnInteger
        page_obj = None
    
    context = {
        'page_obj': page_obj,
        'selected_type': image_type if 'image_type' in locals() else 'all',
        'selected_category': category if 'category' in locals() else '',
    }
    return render(request, 'reports/gallery.html', context)


def safety_tips_view(request):
    """Safety tips page"""
    return render(request, 'reports/safety_tips.html')


@login_required
def save_zone_view(request):
    """Save a risk zone"""
    if request.method == 'POST':
        form = SavedZoneForm(request.POST)
        if form.is_valid():
            zone = form.save(commit=False)
            zone.user = request.user
            zone.save()
            messages.success(request, 'Zone saved successfully!')
            return redirect('reports:dashboard')
    else:
        form = SavedZoneForm()
    
    return render(request, 'reports/save_zone.html', {'form': form})


def get_incidents_json(request):
    """API endpoint for getting incidents as JSON (for map)"""
    reports = IncidentReport.objects.filter(is_verified=True)
    
    incidents = []
    for report in reports:
        incidents.append({
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'severity': report.severity,
            'latitude': float(report.latitude),
            'longitude': float(report.longitude),
            'location_name': report.location_name or '',
            'incident_date': report.incident_date.isoformat(),
        })
    
    return JsonResponse({'incidents': incidents})


@login_required
def community_discussion_view(request):
    """Community discussion page"""
    try:
        category_filter = request.GET.get('category', 'all')
        
        discussions = CommunityDiscussion.objects.all().select_related('user').order_by('-created_at')
        
        if category_filter != 'all':
            discussions = discussions.filter(category=category_filter)
        
        # Pagination
        paginator = Paginator(discussions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        # If database tables don't exist yet, use empty defaults
        page_obj = None
        category_filter = 'all'
    
    context = {
        'page_obj': page_obj,
        'selected_category': category_filter,
    }
    return render(request, 'reports/community.html', context)


@login_required
def create_discussion_view(request):
    """Create a new discussion post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category', 'general')
        
        if title and content:
            discussion = CommunityDiscussion.objects.create(
                user=request.user,
                title=title,
                content=content,
                category=category
            )
            messages.success(request, 'Discussion post created successfully!')
            return redirect('reports:community')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('reports:community')


@login_required
def discussion_detail_view(request, discussion_id):
    """View a discussion post and its replies"""
    discussion = get_object_or_404(CommunityDiscussion, id=discussion_id)
    replies = discussion.replies.all().select_related('user').order_by('created_at')
    
    if request.method == 'POST':
        content = request.POST.get('reply_content')
        if content:
            DiscussionReply.objects.create(
                discussion=discussion,
                user=request.user,
                content=content
            )
            discussion.reply_count = discussion.replies.count()
            discussion.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('reports:discussion_detail', discussion_id=discussion_id)
    
    context = {
        'discussion': discussion,
        'replies': replies,
    }
    return render(request, 'reports/discussion_detail.html', context)


def privacy_policy_view(request):
    """Privacy Policy page"""
    return render(request, 'reports/privacy_policy.html')


def terms_view(request):
    """Terms of Use page"""
    return render(request, 'reports/terms.html')


def about_view(request):
    """About page"""
    return render(request, 'reports/about.html')

