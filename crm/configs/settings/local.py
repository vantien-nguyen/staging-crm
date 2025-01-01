import os.path

import environ

from configs.settings.common import *

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".envs/local/postgres"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dc^k^(qdgp9ex_kc)dc$5aos(t%201kcaxrp@js!qjuqk$s(b2"

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'OMdcGDHdyxWwKnCNOAtVANqSWEijkyHX',
        'HOST': 'postgres.railway.internal',
        'PORT': '5432',
    }
}
