"""
URL configuration for saferoute project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reports.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    # #region agent log
    import json
    import datetime
    import pathlib
    try:
        _storage_setting = getattr(settings, 'STATICFILES_STORAGE', None)
        from pathlib import Path
        log_path = Path(__file__).resolve().parent.parent / '.cursor' / 'debug.log'
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix-v2","hypothesisId":"B","location":"urls.py:15","message":"DEBUG mode static file serving setup","data":{"static_url":settings.STATIC_URL,"static_root":str(settings.STATIC_ROOT),"staticfiles_storage":str(_storage_setting),"staticfiles_storage_type":str(type(_storage_setting)),"debug":settings.DEBUG},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
    except Exception as e:
        try:
            from pathlib import Path
            log_path = Path(__file__).resolve().parent.parent / '.cursor' / 'debug.log'
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix-v2","hypothesisId":"B","location":"urls.py:15","message":"Error in static file setup","data":{"error":str(e)},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
        except: pass
    # #endregion
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

