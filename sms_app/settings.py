import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# set the url since its required
STATIC_URL = 'static/'

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sms_app'
]

# define the database settings
if 'DJANGO_ADMIN_USERNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['DEFAULT_DB_NAME'],
            'USER': os.environ['DEFAULT_DB_USER'],
            'PASSWORD': os.environ['DEFAULT_DB_PASS'],
            'HOST': os.environ['DEFAULT_DB_HOST'],
            'PORT': os.environ['DEFAULT_DB_PORT']
        },
    }
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fao_sms',
            'USER': 'root',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '',
        },
    }
    SECRET_KEY = '@%z0@a8i%_j7zdb9*4+tb)$!_na+91b--@52q^1b!#nq&0t@jn'

# django middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/django')],
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

ROOT_URLCONF = 'sms_app.urls'

# our custom settings

SMS_VALIDITY = 48   # the number of hours an SMS is valid since it was queued

# The default port to serve the application from
DEFAULT_PORT = 9016

SMS_GATEWAYS = {
    'default': 'at',            # the id of the gateway to use as a default. Select from the gateways listed below
    'gateways_priority': [],    # the priority of the listed gateways, if not defined, the gateways will be selected randomly

    'gateways': {
        'infobip': {},
        'at': {},
        'nexmo': {}
    }
}
