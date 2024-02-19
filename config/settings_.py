"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 4.2.
"""

from pathlib import Path
import os


# Read the .env file and load the environment variables
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.append(os.path.join(BASE_DIR, 'apps'))

from .apps import *

for app_path in APPLICATION_BATH:
    sys.path.append(app_path)

AUTH_USER_MODEL
REST_FRAMEWORK
CORS_ALLOWED_ORIGINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['darwashco.com', 'www.darwashco.com','*']

# if DEBUG:
#     ALLOWED_HOSTS += ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS += INSTALLED_HOME_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE += APPS_MIDDLEWARE


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'homepage.context_processors.site_information',
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

    # 'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': config('DB_NAME'),
    #         'USER': config('DB_USER'),
    #         'PASSWORD': config('DB_PASSWORD'),
    #         'HOST': config('DB_HOST'),
    #         'PORT': config('DB_PORT'),
    #     }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "/static/"

# URL prefix for static files.
STATIC_URL = '/static/'

# Define the directory where your static files will be collected.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Replace 'staticfiles' with your desired directory name


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    STATIC_ROOT = config('STATIC_ROOT')


# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),  
]


# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WEBISTE_NAME = config('WEBISTE_NAME')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# print(config('EMAIL_HOST'))



if DEBUG:
    try:
        import debug_toolbar
        MIDDLEWARE += [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            # 'debug_panel.middleware.DebugPanelMiddleware',
        ]
        INTERNAL_IPS = ['127.0.0.1',]
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
        }

    except ImportError:
        pass


# Add the following middleware for development (optional).
if DEBUG:
    MIDDLEWARE += [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]