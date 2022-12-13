# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_saml.utils import get_attribute
from allauth.account.models import EmailAddress
from django_mailman3.models import Profile


"""
Update Django User model using SAML attributes.
"""


def update_user_profile(request):
    given_name = get_attribute(request, 'givenName')
    if given_name is not None:
        request.user.first_name = given_name

    surname = get_attribute(request, 'surname')
    if surname is not None:
        request.user.last_name = surname

    email = get_attribute(request, 'uwEduEmail')
    if email is not None:
        request.user.email = email

    request.user.save(update_fields=['first_name', 'last_name', 'email'])

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if not profile.timezone:
        profile.timezone = getattr(settings, 'TIME_ZONE')
        profile.save()
