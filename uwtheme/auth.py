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
    has_changed = False
    given_name = get_attribute(request, 'givenName')
    if given_name and given_name != request.user.first_name:
        request.user.first_name = given_name
        has_changed = True

    surname = get_attribute(request, 'surname')
    if surname and surname != request.user.last_name:
        request.user.last_name = surname
        has_changed = True

    uw_email = get_attribute(request, 'uwEduEmail')
    if uw_email and uw_email != request.user.email:
        request.user.email = uw_email
        has_changed = True

    if has_changed:
        request.user.save(update_fields=['first_name', 'last_name', 'email'])

    email = get_attribute(request, 'email')
    if email and email != uw_email:
        existing, _ = EmailAddress.objects.get_or_create(
            user=request.user, email__iexact=email, defaults={
                'email': email, 'verified': True})

    profile, _ = Profile.objects.get_or_create(user=request.user)
    if not profile.timezone:
        profile.timezone = getattr(settings, 'PROFILE_TIME_ZONE')
        profile.save()
