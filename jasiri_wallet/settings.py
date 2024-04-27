from pathlib import Path
from . import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    "apps.account",
    "apps.transaction",
    "apps.notification",
    "apps.asset",
    "apps.analytics",
    "apps.adminpanel",
]

CELERY_IMPORTS = [
    "utils.celery_tasks",
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "jasiri_wallet.middlewares.logger.LoggerMiddleware",
]

ROOT_URLCONF = "jasiri_wallet.urls"

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


WSGI_APPLICATION = "jasiri_wallet.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "HOST": env("DB_HOST"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD")
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("CACHE_BROKER_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEV_EMAIL = env("DEV_EMAIL")

COMPANY_EMAIL = env("COMPANY_EMAIL")

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "jasiri_wallet.authentication.UserTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "jasiri_wallet.permissions.Private", 
    ],
    "EXCEPTION_HANDLER": "jasiri_wallet.exceptions_handlers.errors_handler",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    )
}

ALGO_TOKEN = env("ALGO_TOKEN")
TESTNET_ALGO_ENDPOINT = env("TESTNET_ALGO_ENDPOINT")
TESTNET_ALGO_INDEXER_ENDPOINT = env("TESTNET_ALGO_INDEXER_ENDPOINT")
BETANET_ALGO_ENDPOINT = env("BETANET_ALGO_ENDPOINT")
BETANET_ALGO_INDEXER_ENDPOINT = env("BETANET_ALGO_INDEXER_ENDPOINT")
MAINNET_ALGO_ENDPOINT = env("MAINNET_ALGO_ENDPOINT")
MAINNET_ALGO_INDEXER_ENDPOINT = env("MAINNET_ALGO_INDEXER_ENDPOINT")

FIREBASE_KEY = env.json("FIREBASE_KEY")

TWILIO_SID = env("TWILIO_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = env("TWILIO_NUMBER")
TWILIO_SWITCH = env.bool("TWILIO_SWITCH")

CELERY_BROKER_URL = env("CELERY_BROKER_URL")

AWS_DYNAMODB_ACCESS_KEY_ID = env("AWS_DYNAMODB_ACCESS_KEY_ID")
AWS_DYNAMODB_SECRET_ACCESS_KEY = env("AWS_DYNAMODB_SECRET_ACCESS_KEY")
AWS_DYNAMODB_REGION = env("AWS_DYNAMODB_REGION")
AWS_DYNAMODB_TESTNET_TABLE_NAME = env("AWS_DYNAMODB_TESTNET_TABLE_NAME")
AWS_DYNAMODB_MAINNET_TABLE_NAME = env("AWS_DYNAMODB_MAINNET_TABLE_NAME")


AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME") 
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = env("STATIC_URL")
BASE_CDN_URL = env("BASE_CDN_URL")

AFRICAS_TALKING_NUMBER = env("AFRICAS_TALKING_NUMBER")
AFRICAS_TALKING_USERNAME = env("AFRICAS_TALKING_USERNAME")
AFRICAS_TALKING_API_KEY = env("AFRICAS_TALKING_API_KEY")

SERVER = env("SERVER")

NEWS_TTL_MINUTES = env("NEWS_TTL_MINUTES")
JWT_EXPIRATION_DAYS = 30

SMART_CONTRACT_ADDRESS = env("SMART_CONTRACT_ADDRESS")
USERSTACK_KEY = env("USERSTACK_KEY")
ADMIN_ADDRESS = env("ADMIN_ADDRESS")
ADMIN_KEY = env("ADMIN_KEY") 


CONSOLE_SMART_APP_ID = env("CONSOLE_SMART_APP_ID")
CONSOLE_SMART_JSON = env("CONSOLE_SMART_JSON")
TOKENIZATION_SMART_APP_ID = env("TOKENIZATION_SMART_APP_ID")
TOKENIZATION_SMART_JSON = env("TOKENIZATION_SMART_JSON")
TITLE_SMART_APP_ID = env("TITLE_SMART_APP_ID")
TITLE_SMART_JSON = env("TITLE_SMART_JSON")

OTP_EXPIRE_TIME = env.float("OTP_EXPIRE_TIME")
OTP_RESEND_TIMEOUT = env.float("OTP_RESEND_TIMEOUT")
OTP_MAX_ATTEMPTS = env.int("OTP_MAX_ATTEMPTS")

BCRYPT_SALT = env("BCRYPT_SALT")
