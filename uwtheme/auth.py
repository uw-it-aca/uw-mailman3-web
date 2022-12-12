# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


"""
Update Django User model using SAML attributes.
"""
def update_user(user, attributes):
    if 'givenName' in attributes:
        user.first_name = attributes.get('givenName')

    if 'surname' in attributes:
        user.last_name = attributes.get('surname')

    if 'email' in attributes:
        user.email = attributes.get('email')

    user.save(update_fields=['first_name', 'last_name', 'email'])
