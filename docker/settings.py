from .base_settings import *
import os
from socket import gethostbyname

DEBUG = True

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
    'mmtheme',
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

MIDDLEWARE += [
    'postorius.middleware.PostoriusMiddleware'
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
MAILMAN_REST_API_URL = os.environ.get('MAILMAN_REST_URL', 'http://uw-mailman3-core:8001')
MAILMAN_REST_API_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
MAILMAN_REST_API_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')
MAILMAN_ARCHIVER_KEY = os.environ.get('HYPERKITTY_API_KEY')
MAILMAN_ARCHIVER_FROM = os.environ.get('MAILMAN_ARCHIVER_FROM')


MAILMAN_WEB_SOCIAL_AUTH = [
    'django_mailman3.lib.auth.fedora',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1  # Needed for django-allauth

LOGIN_URL = os.environ.get('LOGIN_URL', 'account_login')
LOGOUT_URL = os.environ.get('LOGOUT_URL', 'account_logout')

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
