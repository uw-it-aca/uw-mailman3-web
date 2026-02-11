#
#  The mailman_client methods are necessary to support iteration
#  over a set of mailman core servers that are deployed to implement
#  horizontal scaling.
#

from django.conf import settings
from django_mailman3.lib.mailman import get_request_hooks
from mailmanclient import Client as MailmanClient
from urllib.error import HTTPError
import logging


logger = logging.getLogger(__name__)


def _get_mailman_client(api_url, api_user, api_pass, api_version='3.1'):
    """ Mailman Client for specific Mailman instance. """
    return MailmanClient(
        f"{api_url}/{api_version}",
        name=api_user, password=api_pass,
        request_hooks=get_request_hooks())


def instance_mailman_clients():
    mailman_instances = getattr(settings, 'MAILMAN_CLUSTER', {})
    for web_host, instance in mailman_instances.items():
        api_url = instance.get('api_url')
        api_user = instance.get('api_user')
        api_pass = instance.get('api_pass')

        try:
            logger.debug(f"Connecting {api_url} as {api_user}")
            yield web_host, _get_mailman_client(api_url, api_user, api_pass)
        except HTTPError as ex:
            logger.error(f"Cannot connect to Mailman API at {api_url}: {ex}")
