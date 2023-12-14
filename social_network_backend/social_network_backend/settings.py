"""
Django settings for social_network_backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ni9hq-jpry-(z3pv(pnt1lsn+sq+q6g8ea0di9^_y_w1)a)2-w"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

WEBSITE_URL = os.getenv("WEBSITE_URL")

# Application definition

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTH_USER_MODEL = 'account.User'

SIMPLE_SWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRED"))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv("TOKEN_EXPIRED"))),
    'ROTATE_REFRESH_TOKENS': bool(os.getenv("ROTATE_REFRESH_TOKENS", False))
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

print(os.getenv("CORS_ALLOWED_ORIGINS"))
CORS_ALLOWED_ORIGINS = [allowed for allowed in os.getenv("CORS_ALLOWED_ORIGINS").split(",") if allowed]
CORS_TRUSTED_ORIGINS = [trusted for trusted in os.getenv("CORS_TRUSTED_ORIGINS").split(",") if trusted]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'log_viewer',

    'account',
    'post',
    'search',
    'chat',
    'notification'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_network_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'social_network_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': os.getenv("DATABASE_PORT"),
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

STATIC_URL = os.getenv("STATIC_URL")
MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = BASE_DIR / MEDIA_URL.rstrip('/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORMATTERS = {
    "verbose": {
        "format": "{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
        "style": "{",
    },
    "simple": {
        "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
        "style": "{",
    },
}

# Handler untuk file keseluruhan
all_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/all.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
}

debug_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/debug.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "level": "DEBUG",
}

info_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/info.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "level": "INFO",
}

warning_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/warning.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "level": "WARNING",
}

error_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/error.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "level": "ERROR",
}

critical_handler = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": f"{BASE_DIR}/logs/critical.log",
    "mode": "a",
    "encoding": "utf-8",
    "formatter": "verbose",
    "backupCount": 5,
    "maxBytes": 1024 * 1024 * 5,  # 5 MB
    "level": "CRITICAL",
}

# Kumpulan handler
HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    "all_handler": all_handler,
    "debug_handler": debug_handler,
    "info_handler": info_handler,
    "warning_handler": warning_handler,
    "error_handler": error_handler,
    "critical_handler": critical_handler,
}

LOGGERS = {
    "django": {
        "handlers": [
            "console_handler",
            "all_handler",
            "debug_handler",
            "info_handler",
            "error_handler",
            "warning_handler",
            "critical_handler"
        ],
        "level": "INFO",
        "propagate": False,
    },
    "django.request": {
        "handlers": ["error_handler"],
        "level": "ERROR",
        "propagate": False,
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS,
    "handlers": HANDLERS,
    "loggers": LOGGERS,
}