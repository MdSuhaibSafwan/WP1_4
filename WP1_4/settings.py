from pathlib import Path
import environ,os
 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

env = environ.Env()
environ.Env.read_env()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h-_d%lmvef2)_ohguq7_g=%-+=b=n6p4!*+hhn3qshc!g%5=d6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['tomsSite.com','127.0.0.1']
#test site
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://localhost:443, https://127.0.0.1:443, https://0.0.0.0:443, https://172.23.141.204:443', 'http://localhost', 'http://127.0.0.1', 'http://0.0.0.0', 'http://172.23.141.204']

CORS_ORIGIN_WHITELIST = ['https://localhost:443, https://127.0.0.1:443, https://0.0.0.0:443, https://172.23.141.204:443', 'http://localhost', 'http://127.0.0.1', 'http://0.0.0.0', 'http://172.23.141.204']

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'Login.apps.LoginConfig',
    'Main.apps.MainConfig',
    'django_celery_beat',
    'Export.apps.ExportConfig',
    'MainData.apps.MaindataConfig',
    'Dashboard.apps.DashboardConfig',
    'Admin.apps.AdminConfig',
    'monorepo.apps.MonorepoConfig',
    'EnergyCapture.apps.EnergycaptureConfig',
    'phonenumber_field',
    'supervisor',
    'guardian',
    'channels',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'WP1_4.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # new
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


WSGI_APPLICATION = 'WP1_4.wsgi.application'
ASGI_APPLICATION = 'WP1_4.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#Dev database:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#     	'OPTIONS': {
#         	'read_default_file': '/etc/mysql/my.cnf',
#     	},
#     },
#     'LION': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'aap',
#         'USER': 'postgres',
#         'PASSWORD': '01',
#         'HOST': '10.10.42.19',
#         'PORT': '5432',
#         'POSTGRES_NAME':"postgres",
#         'POSTGRES_USER':"postgres",
#         'POSTGRES_PASSWORD' : "01",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3"
    }
}

#Docker database
#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.mysql',
   #     'NAME': 'db',
    #    'USER': 'root',
     #   'PASSWORD':'password',
      #  'HOST':'db',
       # 'PORT': '3306',
    #}
#}


CHANNEL_LAYERS= {
    'default': {
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
           #docker layer
            # 'hosts':[('redis', 6379)]
        #dev layer

            'hosts':[('127.0.0.1', 6379)]

        }
    }
}

# Password validation

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DJANGO_CELERY_BEAT_TZ_AWARE = False


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'Main/static/')
]



#redirects for login pages

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/mylogout"

# settings to deal with the contact form email
# settings to deal with the contact form email
#DEV celery specs
# CELERY_BROKER_URL = "redis://127.0.0.1:6379"
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
# celery setting.
CELERY_CACHE_BACKEND = 'default'

#Docker celery specs
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'p-4 mb-4 text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'p-4 mb-4 text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800',
}

