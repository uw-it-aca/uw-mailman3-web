from .base_settings import *
import os
from socket import gethostbyname

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

# Mailman API credentials
MAILMAN_REST_API_URL = os.environ.get('MAILMAN_REST_URL', 'http://mailman-core:8001')
MAILMAN_REST_API_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
MAILMAN_REST_API_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')
MAILMAN_ARCHIVER_KEY = os.environ.get('HYPERKITTY_API_KEY')
#MAILMAN_ARCHIVER_FROM = (os.environ.get('MAILMAN_HOST_IP', gethostbyname(os.environ.get('MAILMAN_HOSTNAME', 'mailman-core'))),)
MAILMAN_ARCHIVER_FROM = '172.19.199.2'

MAILMAN_WEB_SOCIAL_AUTH = [
    'django_mailman3.lib.auth.fedora',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
]

SITE_ID =1  # Needed for django-allauth

TEMPLATES[0]["OPTIONS"]["context_processors"].extend([
	# Required by allauth template tags
	"django.template.context_processors.request",
	# allauth specific context processors
	"allauth.account.context_processors.account",
	"allauth.socialaccount.context_processors.socialaccount",
])
