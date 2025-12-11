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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

# Media files
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

