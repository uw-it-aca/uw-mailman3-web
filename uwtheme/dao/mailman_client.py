

from django.conf import settings
from mailmanclient import Client as MailmanClient
from django_mailman3.lib.mailman import get_request_hooks
from django.core.cache import cache
from urllib.error import HTTPError
import sys
import logging


logger = logging.getLogger(__name__)


def _get_mailman_client(api_url, api_user, api_pass, api_version='3.1'):
    """ Mailman Client for specific Mailman instance. """
    return MailmanClient(
        f"{api_url}/{api_version}",
        name=api_user, password=api_pass,
        request_hooks=get_request_hooks())


def _get_mailman_user(mm_client, user):
    """Given a Django user, return the Mailman's user object.

    If the user does not exist, we will try to create one.  If neither of the
    get or create options work, perhaps because API is un-reachable, we return
    a None value.

    :param user: Instance of a Django user.
    :returns: Mailman user or None if Mailman API isn't available.
    :rtype: :class:`mailmanclient.User`
    """
    # Only cache the mailman user_id, not the whole user instance, because
    # mailmanclient is not pickle-safe
    cache_key = "User:%s:mailman_user_id" % user.id
    mm_user_id = cache.get(cache_key)
    try:
        mm_user = None
        if mm_user_id is not None:
            # Due upgrade from Mailman API 3.0 to 3.1, integer user_id can
            # return 404 if the API version used was 3.1 (which has user_ids as
            # UUIDs). So, we are going to lookup with email if the cached
            # user_id returns 404.
            try:
                mm_user = mm_client.get_user(mm_user_id)
            except HTTPError as e:
                if e.code != 404:
                    raise
        # So, either the user_id wasn't cached or the cached user_id didn't
        # return a valid user. Now lookup with user's email.
        if mm_user is None:
            try:
                mm_user = mm_client.get_user(user.email)
            except HTTPError as e:
                if e.code != 404:
                    raise  # will be caught down there
                mm_user = mm_client.create_user(
                    user.email, user.get_full_name())
                # XXX The email is not set as verified, because we don't
                # know if the registration that was used verified it.
                logger.info("Created Mailman user for %s (%s)",
                            user.username, user.email)
            # Update the cache to avoid a lookup next time.
            cache.set(cache_key, mm_user.user_id, None)
        return mm_user
    except (HTTPError, MailmanConnectionError) as e:
        logger.warning(
            "Error getting or creating the Mailman user of %s (%s): %s",
            user.username, user.email, e)
        return None


def _get_lists_in_instance(instance, username, role):
    api_url = instance.get('api_url')
    api_user = instance.get('api_user')
    api_pass = instance.get('api_pass')

    logger.debug(f"Finding lists for {username} with "
                 f"role {role} in Mailman instance at {api_url}")

    try:
        client = _get_mailman_client(api_url, api_user, api_pass)
        logger.debug(f"Connected to Mailman API at {api_url} as {api_user}")
    except HTTPError as ex:
        logger.error(f"Cannot connect to Mailman API at {api_url}: {ex}")
        return []

    try:
        mm_user = _get_mailman_user(client, username)
        user_id = mm_user.user_id if mm_user else None

        logger.debug(f"mailman_user on {api_url} is {mm_user} ({user_id})")

        instance_lists = client.find_lists(
            user_id, role=role, mail_host=None, count=sys.maxsize)

        logger.debug(f"found {len(instance_lists)} lists for "
                     f"user {username} ({user_id}) "
                     f"with role {role} in "
                     f"Mailman instance at {api_url}")

        return instance_lists

    except HTTPError as ex:
        logger.debug(f"No lists found for user_id={user_id}, "
                     f"role={role}, mail_host={api_url}: {ex}")
        return []

    return []


def find_all_lists(username, role=None, count=100):
    lists = []
    mailman_instances = getattr(settings, 'MAILMAN_CLUSTER', {})

    logger.debug(f"Finding lists for {username} with "
                 f"role {role} across "
                 f"{len(mailman_instances)} Mailman instances")

    for web_host, instance in mailman_instances.items():
        instance_lists = _get_lists_in_instance(instance, username, role)

        logger.debug(f"Found {len(instance_lists)} lists on "
                     f"{instance.get('api_url')}")

        # add web_host to the MailinList object so it can be
        # referenced in the template
        for mlist in instance_lists:
            logger.debug(f"adding web_host {web_host} to "
                         f"list {mlist.list_id}")
            mlist.web_host = web_host

        lists.extend(instance_lists)

    return lists

