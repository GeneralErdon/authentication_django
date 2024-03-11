from datetime import timedelta
from pathlib import Path
from environ import Env

from core.database import get_db_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)


# If debug true, all host allowed
ALLOWED_HOSTS = [
    "*",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    *[f"http://{x}:5173" for x in env.list("DEVELOPING_CORS_ALLOWED")]
]

CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS


ACTIVE_CACHE = env.bool("DJANGO_ACTIVE_CACHE", True)

CACHES = {
    "default": {
        "BACKEND":"django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": Path(BASE_DIR, "django_cache").resolve()
    }
}

CACHE_LIFETIME = 60 * 15 # in seconds


SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),  
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=24),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissions'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        # 'apps.base.filter.FixedSearchFilter',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    )

}


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    "corsheaders",
    "drf_yasg",
    "debug_toolbar",
]

MY_APPS = [
    "core",
    "apps.base",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MY_APPS



MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        **get_db_config("sqlite", BASE_DIR),
        }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = False

AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = "media/"
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media_root"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if not DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
    CORS_ALLOWED_ORIGINS = [f"http://{x}" for x in env.list("PRODUCTION_CORS_ALLOWED")]
    CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS
    
    REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions'
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'apps.base.filter.FixedSearchFilter',
        'rest_framework.filters.OrderingFilter'
    )

}