# -*- coding: utf-8 -*-
# Copyright (C) 1998-2023 by the Free Software Foundation, Inc.
#
# This file is derived from Postorius.
#


import logging
import sys

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from django_mailman3.lib.paginator import MailmanPaginator, paginate

from postorius.views.list import (
    _get_choosable_domains,
    _get_choosable_styles,
    _get_default_style,
    _unique_lists,
    _get_mail_host,
)

from uwtheme.dao.mailman_client.lists import find_all_lists, get_all_list_page


logger = logging.getLogger(__name__)


@login_required
def list_index_authenticated(request):
    """Index page for authenticated users.

    Index page for authenticated users is slightly different than
    un-authenticated ones. Authenticated users will see all their memberships
    in the index page.

    This view is not paginated and will show all the lists.

    """
    role = request.GET.get('role', None)
    #client = get_mailman_client()
    choosable_domains = _get_choosable_domains(request)

    # Get the user_id of the current user
    #user_id = get_mailman_user_id(request.user)

    #mail_host = _get_mail_host(request.get_host().split(':')[0])
    ## Get all the mailing lists for the current user.
    #try:
    #    logger.debug(f"Finding lists for user_id={user_id}, role={role}, mail_host={mail_host}")
    #    all_lists = client.find_lists(
    #        user_id, role=role, mail_host=mail_host, count=sys.maxsize
    #    )
    #except HTTPError as ex:
    #    # No lists exist with the given role for the given user.
    #    logger.debug(f"No lists found for user_id={user_id}, role={role}, mail_host={mail_host}: {ex}")
    #    all_lists = []
    all_lists = find_all_lists(request.user, role=role, count=sys.maxsize)

    # If the user has no list that they are subscriber/owner/moderator of, we
    # just redirect them to the index page with all lists.
    if len(all_lists) == 0 and role is None:
        return redirect(reverse('list_index') + '?all-lists')
    # Render the list index page with `check_advertised = False` since we don't
    # need to check for advertised list given that all the users are related
    # and know about the existence of the list anyway.
    context = {
        'lists': _unique_lists(all_lists),
        'domain_count': len(choosable_domains),
        'role': role,
        'check_advertised': False,
    }
    return render(request, 'uwtheme/postorius/index.html', context)


def _get_list_page(count, page):
    """
    Replace nested function in postorius.views.list_index with function
    to collect lists from all instances
    """
    logger.debug(f"_get_list_page: fetching {count} lists for page {page}")
    advertised = not request.user.is_superuser
    return get_all_list_page(
        count=count, page=page, advertised=advertised)
