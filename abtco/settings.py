import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'www.abtco.us', 'khatynka.abtco.us', 'shop.abtco.us', 'abtco.us',
    'khatynka.localhost', 'shop.localhost', 'www.khatynka.abtco.us',
    'localhost', '127.0.0.1', 'abtcoproject.herokuapp.com'
]

INSTALLED_APPS = [
    'django_hosts',
    'main',
    'sellapp.apps.SellappConfig',
    'khatynka',
    'shop',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'paypal.standard.ipn',
    'crispy_forms',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'abtco.urls'

TEMPLATES = [
    {
        'BACKEND':
        'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'TEMPLATES'),
            os.path.join(BASE_DIR, 'khatynka/templates'),
            os.path.join(BASE_DIR, 'shop/templates'),
            os.path.join(BASE_DIR, 'main/templates'),
            os.path.join(BASE_DIR, 'abtco/main/templates'),
            os.path.join(BASE_DIR, 'users/templates'),
        ],
        'APP_DIRS':
        True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django_hosts.templatetags.hosts_override',
            ]
        },
    },
]

WSGI_APPLICATION = 'abtco.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

PAYPAL_RECEIVER_EMAIL = 'abt.company@aol.com'
PAYPAL_TEST = False

PAYPAL_RECEIVER_EMAIL = 'abt.company-facilitator@aol.com'
PAYPAL_TEST = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = 'loginn'


def debug_env_var(name):
    try:
        with open(
                rf'D:\libraries\Desktop\Dj\env\Scripts\app\abtco_env\{name}.txt'
        ) as file:
            return file.read()
    except:
        pass


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abtcous2014@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_USER',
                                     debug_env_var('EMAIL_HOST_USER'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'

ROOT_HOSTCONF = 'main.hosts'
DEFAULT_HOST = 'www'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
