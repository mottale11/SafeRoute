"""
Django settings for saferoute project.
"""

from pathlib import Path
import os
import json
import datetime

# Optional import for dj_database_url (only needed if DATABASE_URL is set)
try:
    import dj_database_url
except ImportError:
    dj_database_url = None
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# #region agent log
try:
    import pathlib
    log_path = BASE_DIR / '.cursor' / 'debug.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"settings.py:20","message":"Settings module imported","data":{"timestamp":datetime.datetime.now().isoformat(),"base_dir":str(BASE_DIR)},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
except Exception as e:
    try:
        import pathlib
        log_path = BASE_DIR / '.cursor' / 'debug.log'
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"settings.py:20","message":"Settings import log error","data":{"error":str(e)},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
    except: pass
# #endregion


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production-xyz123')

# SECURITY WARNING: don't run with debug turned on in production!
# Default to True for development, set DJANGO_DEBUG=0 to disable
DEBUG = os.environ.get('DJANGO_DEBUG', '1').lower() in ['1', 'true', 'yes']

_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if _render_host:
    ALLOWED_HOSTS = [
        _render_host,
        '.onrender.com',
    ]

CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Must be before 'django.contrib.staticfiles'
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    'reports',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saferoute.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'saferoute.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    if dj_database_url is None:
        raise ImportError(
            "dj_database_url is required when DATABASE_URL is set. "
            "Install it with: pip install dj-database-url"
        )
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    # Try PostgreSQL first, fall back to SQLite if not configured
    db_name = os.environ.get('DB_NAME', 'saferoute_db')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    
    # Use SQLite for development if PostgreSQL password is not set
    if not db_password:
        # #region agent log
        try:
            log_path = BASE_DIR / '.cursor' / 'debug.log'
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"db-fix","hypothesisId":"D","location":"settings.py:130","message":"Using SQLite database (PostgreSQL password not set)","data":{"db_engine":"sqlite3"},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        # #region agent log
        try:
            log_path = BASE_DIR / '.cursor' / 'debug.log'
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"db-fix","hypothesisId":"D","location":"settings.py:145","message":"Using PostgreSQL database","data":{"db_engine":"postgresql","db_name":db_name,"db_user":db_user,"db_host":db_host},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Note: STATICFILES_STORAGE removed - WhiteNoise handles static files at middleware level
# For production with WhiteNoise, you can optionally set:
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# #region agent log
try:
    import pathlib
    log_path = BASE_DIR / '.cursor' / 'debug.log'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix-v2","hypothesisId":"C","location":"settings.py:157","message":"STATICFILES_STORAGE removed - using WhiteNoise middleware","data":{"whitenoise_in_middleware":'whitenoise.middleware.WhiteNoiseMiddleware' in MIDDLEWARE,"static_url":STATIC_URL,"static_root":str(STATIC_ROOT)},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
except Exception as e:
    try:
        import pathlib
        log_path = BASE_DIR / '.cursor' / 'debug.log'
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix-v2","hypothesisId":"C","location":"settings.py:157","message":"Static files config log error","data":{"error":str(e)},"timestamp":int(datetime.datetime.now().timestamp()*1000)})+'\n')
    except: pass
# #endregion

# Media files - Cloudinary Configuration
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
    'SECURE': True,
}

# Initialize Cloudinary if available and configured
if CLOUDINARY_AVAILABLE and CLOUDINARY_STORAGE['CLOUD_NAME']:
    cloudinary.config(
        cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=CLOUDINARY_STORAGE['API_KEY'],
        api_secret=CLOUDINARY_STORAGE['API_SECRET'],
        secure=True
    )

# Use Cloudinary for media files if configured, otherwise use local storage
if CLOUDINARY_AVAILABLE and CLOUDINARY_STORAGE['CLOUD_NAME']:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    # Fallback to local storage if Cloudinary not configured
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'reports:dashboard'
LOGOUT_REDIRECT_URL = 'reports:home'

# Security & proxies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Django Jazzmin Configuration
JAZZMIN_SETTINGS = {
    # Title on the brand (19 chars max)
    "site_title": "SafeRoute Admin",
    
    # Title on the login screen (19 chars max)
    "site_header": "SafeRoute",
    
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SafeRoute",
    
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/SR_Logo.png",
    
    # Logo to use for your site, must be present in static files, used for login form logo
    "login_logo": "images/SR_Logo.png",
    
    # Logo to use for login form in dark themes
    "login_logo_dark": None,
    
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    
    # Welcome text on the login screen
    "welcome_sign": "Welcome to SafeRoute Administration",
    
    # Copyright on the footer
    "copyright": "SafeRoute",
    
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": ["accounts.CustomUser", "reports.IncidentReport"],
    
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        
        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        
        # model admin to link to (Permissions checked against model)
        {"model": "accounts.CustomUser"},
        
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "reports"},
    ],
    
    #############
    # User Menu #
    #############
    
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "auth.user"}
    ],
    
    #############
    # Side Menu #
    #############
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to aut expand the menu
    "navigation_expanded": True,
    
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["accounts", "reports"],
    
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "reports": [{
            "name": "View Reports Dashboard",
            "url": "/",
            "icon": "fas fa-chart-line",
            "new_window": True,
        }]
    },
    
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.1.0,5.2.0,5.3.0,5.4.0
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.CustomUser": "fas fa-user-shield",
        "reports.IncidentReport": "fas fa-exclamation-triangle",
        "reports.IncidentImage": "fas fa-image",
        "reports.IncidentVideo": "fas fa-video",
        "reports.IncidentAudio": "fas fa-microphone",
        "reports.SavedZone": "fas fa-map-marker-alt",
        "reports.HelpfulReport": "fas fa-thumbs-up",
        "reports.CommunityDiscussion": "fas fa-comments",
        "reports.DiscussionReply": "fas fa-reply",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "admin/css/custom_admin.css",
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

