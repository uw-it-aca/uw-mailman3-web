from .base_settings import *
import os
from socket import gethostbyname

if os.getenv("ENV") != "prod":
    DEBUG = True

ALLOWED_HOSTS = ['*']

SAML_USER_PROFILE_HOOK = 'uwtheme.auth.update_user_profile'

#
# Full-text search engine
#
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': "/opt/mailman-web-data/fulltext_index",
        # You can also use the Xapian engine, it's faster and more accurate,
        # but requires another library.
        # http://django-haystack.readthedocs.io/en/v2.4.1/installing_search_engines.html#xapian
        # Example configuration for Xapian:
        #'ENGINE': 'xapian_backend.XapianEngine'
    },
}

INSTALLED_APPS += [
    'uwtheme',
    'hyperkitty',
    'postorius',
    'django_mailman3',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.sites',  # Needed for django-allauth
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    'rest_framework',
    'django_gravatar',
    'compressor',
    'haystack',  # Full-text search engine
    'django_extensions',
    'django_q',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

if os.getenv('THEME_OFF', 'false') == 'true':
    INSTALLED_APPS.remove('uwtheme')

MIDDLEWARE += [
    'postorius.middleware.PostoriusMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_mailman3.middleware.TimezoneMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

#COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True
COMPRESS_ROOT = '/static/'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', 'sassc -t compressed {infile} {outfile}'),
    ('text/x-sass', 'sassc -t compressed {infile} {outfile}'),
)

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

# Mailman API credentials
MAILMAN_REST_API_URL = os.environ.get(
    'MAILMAN_REST_URL', 'http://uw-mailman3-core:8080')
MAILMAN_REST_API_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
MAILMAN_REST_API_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')
MAILMAN_ARCHIVER_KEY = os.environ.get('HYPERKITTY_API_KEY')
MAILMAN_ARCHIVER_FROM = os.environ.get('MAILMAN_ARCHIVER_FROM')

# postorius
# this is the base for urls that are told to core so it can find templates which live in postorius
POSTORIUS_TEMPLATE_BASE_URL = os.environ.get('POSTORIUS_TEMPLATE_BASE_URL')

SITE_ID = 1  # Needed for django-allauth

LOGIN_URL = os.environ.get('LOGIN_URL', 'account_login')
LOGIN_REDIRECT_URL = 'list_index'
LOGOUT_URL = os.environ.get('LOGOUT_URL', 'account_logout')

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
AUTHENTICATION_BACKENDS += (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',)

Q_CLUSTER = {
    'timeout': 60,
    'save_limit': 100,
    'orm': 'default',
}

TEMPLATES[0]["OPTIONS"]["context_processors"].extend([
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.template.context_processors.csrf',
    'django_mailman3.context_processors.common',
    'hyperkitty.context_processors.common',
    'postorius.context_processors.postorius'
])

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_SSL_CERTFILE = os.getenv('CERT_PATH', '')
EMAIL_SSL_KEYFILE = os.getenv('KEY_PATH', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '')

# set to match core, as long as user has correct-for-them tz then
# dates / times will display correctly
TIME_ZONE = 'UTC'
#
# default time zone for user profiles
PROFILE_TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True
