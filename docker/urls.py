import os
from .base_urls import *
from django.contrib import admin
from django.urls import include, re_path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns += [
    re_path(r'^$', RedirectView.as_view(
        url=reverse_lazy('list_index'),
        permanent=True)),
    re_path(r'^postorius/', include('postorius.urls')),
    re_path(r'^hyperkitty/', include('hyperkitty.urls')),
    re_path(r'', include('django_mailman3.urls')),
    re_path(r'^accounts/', include('allauth.urls')),
    # Django admin
    re_path(r'^admin/', admin.site.urls),
]
