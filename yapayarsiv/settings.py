"""
Django settings for yapayarsiv project (cleaned for public repos).

Sensitive values must be provided via environment variables (.env).
"""

from pathlib import Path
import os
import environ

# Initialize environment variables
env = environ.Env(
    # set casting and default values
    DEBUG=(bool, False),
    TIME_ZONE=(str, "Europe/Istanbul"),
)

# read .env file if present
environ.Env.read_env()

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = env("SECRET_KEY")  # MUST be set in .env
DEBUG = env.bool("DEBUG", default=False)

# Hosts
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["yapayarsiv.com", "kurs.yapayarsiv.com", "egitim.yapayarsiv.com", "www.yapayarsiv.com"],
)

# Optional: site domain and cookie domain via env
SITE_DOMAIN = env("SITE_DOMAIN", default="yapayarsiv.com")
SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN", default=SITE_DOMAIN)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "users",
    "tools",
    "forum",
    "course",
    "django_quill",
    "rest_framework",
    "django_hosts",
    "social_django",
    "django_cleanup",
    "crispy_forms",
    "ckeditor",
    "crispy_bootstrap5",
    "django_ckeditor_5",
    "infscroll",
]

SITE_ID = env.int("SITE_ID", default=1)

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

ROOT_URLCONF = "yapayarsiv.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "course.context_processors.loadSettings",
            ],
        },
    },
]

WSGI_APPLICATION = "yapayarsiv.wsgi.application"

# Database (use env vars)
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("DB_NAME", default=""),
        "USER": env("DB_USER", default=""),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# REST framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 9,
}

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="tr")
TIME_ZONE = env("TIME_ZONE", default="Europe/Istanbul")
USE_I18N = True
USE_TZ = True

# Static / Media
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Additional app config
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Security-related flags (set via env when applicable)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=True)
X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="DENY")
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_PROXY_SSL_HEADER = None
if env.bool("USE_X_FORWARDED_PROTO", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Logging (simple file handler — adjust in production)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": env("DJANGO_LOG_FILE", default=os.path.join(BASE_DIR, "django_info.log")),
        },
    },
    "root": {"handlers": ["file"], "level": "INFO"},
}

# CKEditor / Quill config (unchanged)
CKEDITOR_CONFIGS = {
    "default": {
        "versionCheck": False,
        "toolbar": "full",
        "width": "100%",
        "removePlugins": "stylesheetparser",
        "allowedContent": True,
    }
}
CKEDITOR_UPLOAD_PATH = "course/ckeditor"
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Auth / Login URLs
LOGIN_URL = "user:login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_URL = "user:logout"
LOGOUT_REDIRECT_URL = "user:login"

# Custom app settings (use env or defaults)
tools_paging_number = env.int("TOOLS_PAGING_NUMBER", default=20)
posts_paging_number = env.int("POSTS_PAGING_NUMBER", default=12)
general_settings_cache_path = BASE_DIR / "cache_logs" / "general_settings.json"
join_images_path = BASE_DIR / "static" / "payment_page_images"

# Hosts and site config
ROOT_HOSTCONF = env("ROOT_HOSTCONF", default="yapayarsiv.hosts")
DEFAULT_HOST = env("DEFAULT_HOST", default="root")
AUTH_USER_MODEL = "users.CustomUser"

# PAYTR credentials (must be provided in env)
PAYTR_MERCHANT_ID = env("PAYTR_MERCHANT_ID", default=None)
PAYTR_MERCHANT_KEY = env("PAYTR_MERCHANT_KEY", default=None)
PAYTR_MERCHANT_SALT = env("PAYTR_MERCHANT_SALT", default=None)
PAYTR_TEST_MODE = env.bool("PAYTR_TEST_MODE", default=False)

# Social auth (Google) — from env
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default=None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default=None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email"]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Email (use env)
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.hostinger.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=465)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default=None)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

# Sentry (init only when SENTRY_DSN provided)
SENTRY_DSN = env("SENTRY_DSN", default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.1),
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE", default=0.0),
    )

# Misc site settings (default values kept, but can be overridden)
site_domain = SITE_DOMAIN
http_protocol = env("HTTP_PROTOCOL", default="https")
course_domain = env("COURSE_DOMAIN", default="kurs." + SITE_DOMAIN)
course_site_price = env.float("COURSE_SITE_PRICE", default=2499.0)

# Other small configs
QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"font": []},
                    {"header": []},
                    {"align": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                    {"color": []},
                    {"background": []},
                ],
                ["code-block", "link"],
                ["clean"],
            ],
        },
    }
}
