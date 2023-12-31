import os
from pathlib import Path
import firebase_admin
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#ff!55^%&1)!j1&=!=@_u20g*!^j+-ijp@lay6%k0n*m(v9icb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    "debug_toolbar",
    'rest_framework',
    'drf_yasg',
    'rest_framework.authtoken',
    'django_filters',
    'accounts',
    'venues',
    'events',
    'posts',
]

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    # "dark_mode_theme": "darkly",
}
JAZZMIN_SETTINGS = {
    "show_ui_builder": True,
    "site_title": "Eventasya Administration",
    "site_header": "Eventasya",
    "welcome_sign": "Welcome to Eventasya",

    # Copyright on the footer
    "copyright": "Eventasya",
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.user": "fas fa-user",
        "accounts.normal_user": "fa-solid fa-user-tie",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "errors",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    "DEFAULT_THROTTLE_CLASSES": [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    "DEFAULT_THROTTLE_RATES": {
        'anon': '5/minute',
        'user': '10/minute',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Eventasya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Eventasya.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD': 'PgTONTm4qfCjZrdQxOJ8',
        'HOST': 'containers-us-west-118.railway.app',  # Usually 'localhost' for local development
        'PORT': '6717',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'railway',
        # 'USER': 'postgres',
        # 'PASSWORD': 'QdhUEMjvELGvBzyn1ics',
        # 'HOST': 'containers-us-west-45.railway.app',  # Usually 'localhost' for local development
        # 'PORT': '6920',
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

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_FROM = 'Eventasya Platform <eventasyaplatform@gmail.com>'
# EMAIL_BCC = os.environ.get('EMAIL_BCC') or ''
# #
# EMAIL_HOST = 'smtp-relay.sendinblue.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or 'eventasyaplatform@gmail.com'
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or 'PGUq0SnkVc9Xvh5N'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dn6wxyqha",
    'API_KEY': "282187191632465",
    'API_SECRET': "T0EvHG57uh6d86nPcrF_9HBWkms"
}

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']  # Add your IP address(es) for development environment

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,  # Enable the toolbar only in debug mode
    # Other configuration options...
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    'https://eventasya.onrender.com',
]
import firebase_admin
from firebase_admin import credentials

# Configure the storage bucket URL
cred = credentials.Certificate("eventasya-platform-firebase.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'eventasya-platform-app.appspot.com'
})
FIREBASE_STORAGE_BUCKET = 'eventasya-platform-app.appspot.com'
