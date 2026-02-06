# -*- coding: utf-8 -*-
# Copyright (C) 1998-2023 by the Free Software Foundation, Inc.
#
# This file is derived from Postorius.
#


import logging
import sys
from urllib.error import HTTPError

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from django_mailman3.lib.mailman import (
    get_mailman_client,
    get_mailman_user,
    get_mailman_user_id,
)
from django_mailman3.lib.paginator import MailmanPaginator, paginate
from django_mailman3.models import MailDomain

from postorius.models import (
    Domain,
    Style,
)

from uwtheme.dao.mailman_client import find_all_lists


def _get_choosable_domains(request):
    domains = Domain.objects.all()
    return [(d.mail_host, d.mail_host) for d in domains]


def _get_choosable_styles(request):
    styles = Style.objects.all()
    options = [
        (style['name'], style['description']) for style in styles['styles']
    ]
    return options


def _get_default_style():
    return Style.objects.all()['default']


def _unique_lists(lists):
    """Return unique lists from a list of mailing lists."""
    return {mlist.list_id: mlist for mlist in lists}.values()


def _get_mail_host(web_host):
    """Get the mail_host for a web_host if FILTER_VHOST is true and there's
    only one mail_host for this web_host.
    """
    if not getattr(settings, 'FILTER_VHOST', False):
        return None
    mail_hosts = []
    use_web_host = False
    for domain in Domain.objects.all():
        try:
            if (
                MailDomain.objects.get(
                    mail_domain=domain.mail_host
                ).site.domain
                == web_host
            ):
                if domain.mail_host not in mail_hosts:
                    mail_hosts.append(domain.mail_host)
        except MailDomain.DoesNotExist:
            use_web_host = True
    if len(mail_hosts) == 1:
        return mail_hosts[0]
    elif len(mail_hosts) == 0 and use_web_host:
        return web_host
    else:
        return None


@login_required
def list_index_authenticated(request):
    """Index page for authenticated users.

    Index page for authenticated users is slightly different than
    un-authenticated ones. Authenticated users will see all their memberships
    in the index page.

    This view is not paginated and will show all the lists.

    """
    role = request.GET.get('role', None)
    client = get_mailman_client()
    choosable_domains = _get_choosable_domains(request)

    # Get the user_id of the current user
    user_id = get_mailman_user_id(request.user)

    mail_host = _get_mail_host(request.get_host().split(':')[0])
    # Get all the mailing lists for the current user.
    try:
        all_lists = client.find_lists(
            user_id, role=role, mail_host=mail_host, count=sys.maxsize
        )
    except HTTPError:
        # No lists exist with the given role for the given user.
        all_lists = []
    #all_lists = find_all_lists(user_id, role=role, count=sys.maxsize)

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


def list_index(request, template='uwtheme/postorius/index.html'):
    """Show a table of all public mailing lists."""
    # TODO maxking: Figure out why does this view accept POST request and why
    # can't it be just a GET with list parameter.
    if request.method == 'POST':
        return redirect('list_summary', list_id=request.POST['list'])
    # If the user is logged-in, show them only related lists in the index,
    # except role is present in requests.GET.
    if request.user.is_authenticated and 'all-lists' not in request.GET:
        return list_index_authenticated(request)

    def _get_list_page(count, page):
        client = get_mailman_client()
        advertised = not request.user.is_superuser
        mail_host = _get_mail_host(request.get_host().split(':')[0])
        return client.get_list_page(
            advertised=advertised, mail_host=mail_host, count=count, page=page
        )

    lists = paginate(
        _get_list_page,
        request.GET.get('page'),
        request.GET.get('count'),
        paginator_class=MailmanPaginator,
    )

    # This is just an optimization to skip un-necessary API
    # calls. uwtheme/postorius/index.html page shows the 'Create New Domain'
    # button
    # when the logged-in user is a super user. There is no point making those
    # API calls if the user isn't a Superuser. So, just call the number 0 if
    # the user isn't SU.
    if request.user.is_superuser:
        domain_count = len(_get_choosable_domains(request))
    else:
        domain_count = 0

    return render(
        request,
        template,
        {
            'lists': lists,
            'check_advertised': True,
            'all_lists': True,
            'domain_count': domain_count,
        },
    )
