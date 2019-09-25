import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# set the url since its required
STATIC_URL = 'static/'

ALLOWED_HOSTS = ["*"]

SECRET_KEY = '@z0@a8_j+tb)$_na+91b-@52q^1b#nq&0t@jn'

# use timezones
USE_TZ = True

TIMEZONE = 'Africa/Nairobi'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',
    'rest_framework',
    'sms_app'
]

# define the database settings
if 'DJANGO_ADMIN_USERNAME' in os.environ:
    print("using os.environ variables...")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['DEFAULT_DB_NAME'],
            'USER': os.environ['DEFAULT_DB_USER'],
            'PASSWORD': os.environ['DEFAULT_DB_PASS'],
            'HOST': os.environ['DEFAULT_DB_HOST'],
            'PORT': os.environ['DEFAULT_DB_PORT'],
            'TIMEZONE': 'Africa/Nairobi'
        },
    }

    SMS_GATEWAYS = {
        'default': 'at',            # the id of the gateway to use as a default. Select from the gateways listed below
        'gateways_priority': [],    # the priority of the listed gateways, if not defined, the gateways will be selected randomly

        'gateways': {
            # 'infobip': {},
            'at': {
                'KEY': os.environ['AT_KEY'],
                'ENDPOINT': 'https://api.sandbox.africastalking.com/version1/messaging',
                'USERNAME': os.environ['AT_USERNAME']
            },
            'nexmo': {
                'KEY': os.environ['NEXMO_KEY'],
                'SECRET': os.environ['NEXMO_SECRET'],
            }
        }
    }

    SENTRY_DSN = 'https://%s:%s@sentry.badili.co.ke/7?verify_ssl=0' % (os.environ['SENTRY_USER'], os.environ['SENTRY_PASS'])

else:
    print("using locally defined variables...")
    import environ
    env = environ.Env(
        DEBUG=(bool, False)
    )
    # reading .env file
    environ.Env.read_env()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fao_sms',
            'USER': 'root',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '',
            'TIMEZONE': 'Africa/Nairobi'
        },
    }

    SMS_GATEWAYS = {
        'default': 'at',            # the id of the gateway to use as a default. Select from the gateways listed below
        'gateways_priority': [],    # the priority of the listed gateways, if not defined, the gateways will be selected randomly

        'gateways': {
            # 'infobip': {},
            'at': {
                'KEY': env('AT_KEY'),
                'ENDPOINT': 'https://api.sandbox.africastalking.com/version1/messaging',
                'USERNAME': env('AT_USERNAME')
            },
            'nexmo': {
                'KEY': env('NEXMO_KEY'),
                'SECRET': env('NEXMO_SECRET'),
            }
        }
    }
    SENTRY_DSN = 'https://%s:%s@sentry.badili.co.ke/7?verify_ssl=0' % (env('SENTRY_USER'), env('SENTRY_PASS'))

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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ROOT_URLCONF = 'sms_app.urls'

# our custom settings

SMS_VALIDITY = 48   # the number of hours an SMS is valid since it was queued

# The default port to serve the application from
DEFAULT_PORT = 9018

# The maximum length an sms should be. We spare some characters for adding the message page numbers
SMS_MAX_LENGTH = 300

AT_STATUS_CODES = {
    100: "Processed",
    101: "Sent",
    102: "Queued",
    401: "RiskHold",
    402: "InvalidSenderId",
    403: "InvalidPhoneNumber",
    404: "UnsupportedNumberType",
    405: "InsufficientBalance",
    406: "UserInBlacklist",
    407: "CouldNotRoute",
    500: "InternalServerError",
    501: "GatewayError",
    502: "RejectedByGateway"
}

AT_FAILURE_REASON = {
    'InsufficientCredit': "This occurs when the subscriber doesn’t have enough airtime for a premium subscription service/message",
    'InvalidLinkId': "This occurs when a message is sent with an invalid linkId for an onDemand service",
    'UserIsInactive': "This occurs when the subscriber is inactive or the account deactivated by the MSP (Mobile Service Provider).",
    'UserInBlackList': "This occurs if the user has been blacklisted not to receive messages from a paricular service (shortcode or keyword)",
    'UserAccountSuspended': "This occurs when the mobile subscriber has been suspended by the MSP.",
    'NotNetworkSubcriber': "This occurs when the message is passed to an MSP where the subscriber doesn’t belong.",
    'UserNotSubscribedToProduct': "This occurs when the message from a subscription product is sent to a phone number that has not subscribed to the product.",
    'UserDoesNotExist': "This occurs when the message is sent to a non-existent mobile number.",
    'DeliveryFailure': "This occurs when message delivery fails for any reason not listed above or where the MSP didn’t provide a delivery failure reason.",
}

AT_FINAL_DELIVERY_STATUS = ['Rejected', 'Success', 'Failed']

# nexmo SMS codes as defined https://developer.nexmo.com/messaging/sms/guides/troubleshooting-sms
NEXMO_STATUS_CODES = {
    0: 'Success',                               # The message was successfully accepted for delivery.
    1: 'Throttled',                             # You are sending SMS faster than the account limit (see What is the Throughput Limit for Outbound SMS?).
    2: 'Missing Parameters',                    # Your request is missing one of the required parameters: from, to, api_key, api_secret or text.
    3: 'Invalid Parameters',                    # The value of one or more parameters is invalid.
    4: 'Invalid Credentials',                   # Your API key and/or secret are incorrect, invalid or disabled.
    5: 'Internal Error',                        # An error has occurred in the platform whilst processing this message.
    6: 'Invalid Message',                       # The platform was unable to process this message, for example, an unrecognized number prefix.
    7: 'Number Barred',                         # The number you are trying to send messages to is blacklisted and may not receive them.
    8: 'Partner Account Barred',                # Your Nexmo account has been suspended. Contact support@nexmo.com.
    9: 'Partner Quota Violation',               # You do not have sufficient credit to send the message. Top-up and retry.
    10: 'Too Many Existing Binds',              # The number of simultaneous connections to the platform exceeds your account allocation.
    11: 'Account Not Enabled For HTTP',         # This account is not provisioned for the SMS API, you should use SMPP instead.
    12: 'Message Too Long',                     # The message length exceeds the maximum allowed.
    14: 'Invalid Signature',                    # The signature supplied could not be verified.
    15: 'Invalid Sender Address',               # You are using a non-authorized sender ID in the from field. This is most commonly in North America, where a Nexmo long virtual number or short code is required.
    22: 'Invalid Network Code',                 # The network code supplied was either not recognized, or does not match the country of the destination address.
    23: 'Invalid Callback URL',                 # The callback URL supplied was either too long or contained illegal characters.
    29: 'Non-Whitelisted Destination',          # Your Nexmo account is still in demo mode. While in demo mode you must add target numbers to your whitelisted destination list. Top-up your account to remove this limitation.
    32: 'Signature And API Secret Disallowed',  # A signed request may not also present an api_secret.
    33: 'Number De-activated'
}

NEXMO_FINAL_DELIVERY_STATUS = ['delivered', 'failed', 'rejected', 'expired']

# nexmo delivery codes as defined https://developer.nexmo.com/messaging/sms/guides/delivery-receipts
NEXMO_DELIVERY_CODES = {
    0: "Delivered",                            # Message was delivered successfully
    1: "Unknown",                              # Message was not delivered, and no reason could be determined
    2: "Absent Subscriber - Temporary",        # Message was not delivered because handset was temporarily unavailable - retry
    3: "Absent Subscriber - Permanent",        # The number is no longer active and should be removed from your database
    4: "Call Barred by User",                  # This is a permanent error:the number should be removed from your database and the user must contact their network   op:er"ator to remove the bar
    5: "Portability Error",                    # There is an issue relating to portability of the number and you should contact the network operator to resolve it
    6: "Anti-Spam Rejection",                  # The message has been blocked by a carrier's anti-spam filter
    7: "Handset Busy",                         # The handset was not available at the time the message was sent - retry
    8: "Network Error",                        # The message failed due to a network error - retry
    9: "Illegal Number",                       # The user has specifically requested not to receive messages from a specific service
    10: "Illegal Message",                     # There is an error in a message parameter, e.g. wrong encoding flag
    11: "Unroutable",                          # Nexmo cannot find a suitable route to deliver the message - contact support@nexmo.com
    12: "Destination Unreachable",             # A route to the number cannot be found - confirm the recipient's number
    13: "Subscriber Age Restriction",          # The target cannot receive your message due to their age
    14: "Number Blocked by Carrier",           # The recipient should ask their carrier to enable SMS on their plan
    15: "Prepaid Insufficient Funds",          # The recipient is on a prepaid plan and does not have enough credit to receive your message
    99: "General Error",                       # Typically refers to an error in the route - contact support@nexmo.com
}
