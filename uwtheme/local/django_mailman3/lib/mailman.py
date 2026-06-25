# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2023 by the Free Software Foundation, Inc.
#
# This file is derived from Django-Mailman.
#

from uwtheme.dao.mailman_client import instance_mailman_clients
from uwtheme.dao.mailman_client.user import get_mailman_user
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)


def get_subscriptions(user):
    """this function replaces
       django_mailman3/lib/mailman.py:get_subscriptions
    to collect a user's subscriptions across mailman3 instances
    """

    logger.debug("local get_subscriptions")

    # Get subscriptions for the provided Django user.
    def _get_value():
        return dict(_get_subscriptions_for_user(user))

    # TODO: how should this be invalidated? Subscribe to a signal in
    # mailman when a new subscription occurs? Or store in the session?
    return cache.get_or_set(
        "User:%s:subscriptions" % user.id,
        _get_value, 60, version=2)  # 1 minute
    # TODO: increase the cache duration when we have Mailman signals


def _get_subscriptions_for_user(user):
    """
    return list of tuples representing users list memberships
    across mailman3 instances
    """
    subscriptions = []

    for web_host, client in instance_mailman_clients():
        mm_user = get_mailman_user(client, user)
        if mm_user is not None:
            logger.debug("get subscriptions for user "
                         f"{user.username} on {web_host}")

            subscriptions += [
                (member.list_id, member.address)
                for member in mm_user.subscriptions
                if member.role != "nonmember"
            ]

    logger.debug(f"Found {len(subscriptions)} subscriptions "
                 f"for user {user.username}")

    return subscriptions
