# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf.urls import include
from django.urls import re_path
from uwtheme.views.postorius.list import list_index


urlpatterns = [
    re_path(r'^lists/$', list_index, name='uwtheme_list_index'),
]
