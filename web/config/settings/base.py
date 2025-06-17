import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-development-key-change-in-production")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "web.apps.orders",
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = "web.config.urls"

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "EXCEPTION_HANDLER": "web.core.exception_handler.custom_exception_handler",
} 