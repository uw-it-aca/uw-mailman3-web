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
    if given_name:
        request.user.first_name = given_name

    surname = get_attribute(request, 'surname')
    if surname:
        request.user.last_name = surname

    uw_email = get_attribute(request, 'uwEduEmail')
    if uw_email:
        request.user.email = uw_email

    request.user.save(update_fields=['first_name', 'last_name', 'email'])

    email = get_attribute(request, 'email')
    if email and email != uw_email:
        existing, _ = EmailAddress.objects.get_or_create(
            user=request.user, email__iexact=email, defaults={
                'email': email, 'verified': True})

    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not profile.timezone:
        profile.timezone = getattr(settings, 'TIME_ZONE')
        profile.save()
