# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_saml.utils import get_attribute


"""
Update Django User model using SAML attributes.
"""
def update_user_profile(user, request):
    given_name = get_attribute(request, 'givenName')
    if given_name is not None:
        user.first_name = given_name

    surname = get_attribute(request, 'surname')
    if surname is not None:
        user.last_name = surname

    email = get_attribute(request, 'email')
    if email is not None:
        user.email = email

    user.save(update_fields=['first_name', 'last_name', 'email'])
