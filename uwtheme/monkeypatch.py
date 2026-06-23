from django.core.cache import cache
from uwtheme.dao.mailman_client.subscriptions import get_subscriptions
import sys


def monkey_patch():
    mailman_module = sys.modules.get("django_mailman3.lib.mailman")

    if not mailman_module:
        from django_mailman3.lib import mailman as mailman_module

    mailman_module.get_subscriptions = get_subscriptions
