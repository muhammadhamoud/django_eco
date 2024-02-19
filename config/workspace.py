import os
from .settings import BASE_DIR
from decouple import config
from datetime import date
from django.utils.translation import gettext_lazy as _

END_DATE = date(2025,12,31)

EXTENDED_DEBUG = config('DEBUG', cast=bool)

EXTENDED_ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:4200']

APPLICATION_BATH = [
    os.path.join(BASE_DIR, 'apps', 'home'),
    os.path.join(BASE_DIR, 'apps', 'authentication'),
    os.path.join(BASE_DIR, 'apps', 'core'),
    os.path.join(BASE_DIR, 'apps', 'eco'),

    # os.path.join(BASE_DIR, 'apps', 'shop'),
    # os.path.join(BASE_DIR, 'apps', 'plotters'),

    # os.path.join(BASE_DIR, 'apps', 'realestate'),
    # os.path.join(BASE_DIR, 'apps', 'ecommerce'),
]

NEW_APPS = [
    'homepage',
    'core',
    'communication',
    'accounts',
    'warehouse',
    
    # 'plotter',
    
    # 'shop',
    # 'cart',
    # 'orders',
    # 'payment',
    
    # 'address',
    # 'googlemap',
    # 'plotter_payment',
    # 'cart',
    # 'contents',
    # 'store',
    # 'user_profile',
    # 'order',
    # 'shopingcart',
    # 'sample',
]

INTERNAL_APPS = []
for APP in NEW_APPS:
    INTERNAL_APPS.append(F'{APP}.apps.{APP.title()}Config')


EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
    'mptt',
    'stripe',
    'django_countries',
    'parler',
    'rosetta',
    'localflavor',

]

APPS_EXTENDED = EXTERNAL_APPS + INTERNAL_APPS

APPS_URLS = []
for APP in NEW_APPS:
    APPS_URLS.append(f'{APP}.urls')

APPS_MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'core.middleware.ActiveUserMiddleware'
]


if EXTENDED_DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'apps', 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #config('STATIC_ROOT')
    
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        # os.path.join(BASE_DIR, 'apps', 'static'),
    ]

    # STATICFILES_DIRS = [BASE_DIR / "staticfiles",]
    # print(STATIC_ROOT)
    # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # # Extra places for collectstatic to find static files.
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, 'static'),
    # ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),  
]

# COUNTRIES_FLAG_URL =  '/assets/flags'


AUTH_USER_MODEL = 'accounts.CustomUser'
# Number of minutes of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 10

# Number of seconds that we will keep track of inactive users for before 
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],

    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.UserRateThrottle',
    # ],

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DATE_INPUT_FORMATS': ['%Y-%m-%d', '%d/%m/%Y'],
    'TIME_INPUT_FORMATS': ['%H:%M:%S', '%I:%M %p'], 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Set the number of items per page
}


# Config simple jwt as default authentication and pagination
REST_FRAMEWORK.update({
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
})

# Setup JWT expired date
import datetime
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=14),
}

# CORS
# CORS_ORIGIN_ALLOW_ALL = True  # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
# CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development (you can change this in production)

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = "access-control-allow-origin"
# CORS_ALLOW_METHODS = ['GET', 'OPTIONS']  # Allow GET and OPTIONS methods

# For production, you should specify allowed origins explicitly:

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # Add your Angular app's URL here
]
CORS_ALLOW_HEADERS = [
    'content-type', 
    "access-control-allow-origin",
    'authorization', 
    'accept',
    'accept-encoding',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

SITE_ID = 1

if EXTENDED_DEBUG:
    APPS_EXTENDED += [
        'debug_toolbar',
        # 'debug_panel',
    ]

if EXTENDED_DEBUG:
    APPS_MIDDLEWARE +=[
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

CART_SESSION_ID = 'cart'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SECRET_KEY_CONFIG = config('SECRET_KEY')
WEBISTE_NAME = config('WEBISTE_NAME')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# Stripe settings
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY') 
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')    
# STRIPE_WEBHOOK_SECRET=''
STRIPE_API_VERSION =''
# Redis settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

# Google Map settings
GOOGLE_MAPS_API_WEB_KEY = config('GOOGLE_MAPS_API_WEB_KEY')
GOOGLE_MAPS_API_SERVER_KEY = config('GOOGLE_MAPS_API_SERVER_KEY')


CART_SESSION_ID = 'cart'