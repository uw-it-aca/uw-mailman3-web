

from django.conf import settings
from mailmanclient import Client as MailmanClient
from django_mailman3.lib.mailman import get_request_hooks
from urllib.error import HTTPError
import sys
import logging


logger = logging.getLogger(__name__)


def _get_mailman_client(api_url, api_user, api_pass):
    """ Mailman Client for specific Mailman instance. """
    client = MailmanClient(
        api_url, name=api_user, password=api_pass,
        request_hooks=get_request_hooks())

    return client


def _get_lists_in_instance(instance, user_id, role):
    api_url = instance.get('api_url')
    api_user = instance.get('api_user')
    api_pass = instance.get('api_pass')

    logger.debug(f"Finding lists for user_id {user_id} with "
                 f"role {role} in Mailman instance at {api_url}")

    try:
        client = _get_mailman_client(api_url, api_user, api_pass)

        logger.debug(f"Connected to Mailman API at {api_url} as {api_user}")

        instance_lists = client.find_lists(
            user_id, role=role, mail_host=api_url, count=sys.maxsize)

        logger.debug(f"found {len(instance_lists)} lists for "
                     f"user_id {user_id} with role {role} in "
                     f"Mailman instance at {api_url}")

        return instance_lists

    except HTTPError as ex:
        logger.error(f"Cannot connect to Mailman API at {api_url}: {ex}")
        return []

    return []


def find_all_lists(user_id, role=None, count=100):
    lists = []
    mailman_instances = getattr(settings, 'MAILMAN_CLUSTER', {})

    logger.debug(f"Finding lists for user_id {user_id} with role {role} across "
                    f"{len(mailman_instances)} Mailman instances")

    for web_host, instance in mailman_instances.items():
        instance_lists = _get_lists_in_instance(instance, user_id, role)

        # add web_host to the MailinList object so it can be
        # referenced in the template
        for mlist in instance_lists:
            logger.debug(f"adding web_host {web_host} to "
                         f"list {mlist.list_id}")
            mlist.web_host = web_host

        lists.extend(instance_lists)

    return lists

