"""
Django settings for company_management project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
""" 

import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_HOST = "15.207.233.212:8001"
SITE_URL_HTTP = 'http://{}'.format(SITE_HOST)
SITE_URL_HTTPS = 'https://{}'.format(SITE_HOST)
USE_SSL = False
if USE_SSL:
    DEFAULT_SITE_URL = SITE_URL_HTTPS
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE=True
    SECURE_HSTS_SECONDS = 31536000 #1 year, is common
    SECURE_REDIRECT_EXEMPT = [r'^no-ssl/$']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')
else:
   DEFAULT_SITE_URL = SITE_URL_HTTP


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j=lrnm9qeh(cbn4wl@d@gjyt1y8v&h5^-(!c=*v)u%812ddpx6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',

    'admin_menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'user_manage',
    'dtuser_auth',
    'phone_field',
    # 'payment',
    'corsheaders', #registers corheaders as dependency
    'company_app',
    'payments_management',
    'django_twilio',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware", #to listen in on responses
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://15.207.233.212:8001"
]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

ROOT_URLCONF = 'company_management.urls'
AUTH_USER_MODEL = 'user_manage.LoginUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

WSGI_APPLICATION = 'company_management.wsgi.application'


CELERY_BACKEND_URL = 'redis://localhost:6379/0'
CELERY_BROKER_REDIS_URL="redis://localhost:6380"

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'malfati_user2',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'malfati_db',
        'USER': 'postgres',
        'PASSWORD': 'Malfati123Bhooma',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = f'{DEFAULT_SITE_URL}/static/'
MEDIA_URL = f'{DEFAULT_SITE_URL}/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static')
# ]

# MEDIA_URL = '/media/'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
# MEDIAFILES_DIRS = (
#         os.path.join(BASE_DIR, 'media'),
# )

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
}

DISABLE_COLLECTSTATIC=1

EMAIL_CONFIG = "smtp://user@:password@localhost:25"

# CORS_ALLOWED_ORIGINS = ["*"]
# CORS_ALLOW_HEADERS = [
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# ]
CORS_ORIGIN_ALLOW_ALL=True

RAZOR_KEY_ID = "YOUR_KEY_ID"
RAZOR_KEY_SECRET = "YOUR_KEY_SECRET"

ADMIN_USER_ID = 1

# STATIC_URL = f'{DEFAULT_SITE_URL}/staticfiles/'
# MEDIA_URL = f'{DEFAULT_SITE_URL}/mediafiles/'
COMPRESS_ENABLED = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_TO_EMAIL = ''


# TWILIO_ACCOUNT_SID = 'AC710fde2a95d194182b74045bd8766186'
TWILIO_ACCOUNT_SID = 'AC710fde2a95d194182b74045bd8766186'
# TWILIO_AUTH_TOKEN = 'e4429083087c53eb7e8397c1b13e4144'
TWILIO_AUTH_TOKEN = '7ac33a5dffce0630da84b50f826f2e3b'
TWILIO_NUMBER = '+16402237936'
DJANGO_TWILIO_BLACKLIST_CHECK = True


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# ADMIN_LOGO = 'logo.png'

MENU_WEIGHT = {
    'World': 20,
    'Auth': 4,
    'Sample': 5
}

ADMIN_STYLE = {
    'primary-color': '#164B36',
    'secondary-color': '#092117',
    'tertiary-color': '#51B48E'
}
ADMIN_STYLE = {
    'background': 'white',
    'primary-color': '#205280',
    'primary-text': '#d6d5d2',
    'secondary-color': '#3B75AD',
    'secondary-text': 'white',
    'tertiary-color': '#F2F9FC',
    'tertiary-text': 'black',
    'breadcrumb-color': 'whitesmoke',
    'breadcrumb-text': 'black',
    'focus-color': '#eaeaea',
    'focus-text': '#666',
    'primary-button': '#26904A',
    'primary-button-text':' white',
    'secondary-button': '#999',
    'secondary-button-text': 'white',
    'link-color': '#333',
    'link-color-hover': 'lighten($link-color, 20%)',
    'logo-width': 'auto',
    'logo-height': '35px'
}