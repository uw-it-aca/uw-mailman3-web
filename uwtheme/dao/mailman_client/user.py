#
# this method was lifted from django_mailman3/lib/mailman.py
#

from mailmanclient import MailmanConnectionError
from django.core.cache import cache
from urllib.error import HTTPError
import logging


logger = logging.getLogger(__name__)


def get_mailman_user(mm_client, user):
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
