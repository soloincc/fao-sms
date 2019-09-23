import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

ROOT_URLCONF = 'urls'

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
