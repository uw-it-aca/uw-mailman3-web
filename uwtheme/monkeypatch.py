import postorius.views.list
import django_mailman3.lib.mailman
from uwtheme.local.postorius.views.list import (
    list_index, list_index_authenticated)
from uwtheme.local.django_mailman3.lib.mailman import get_subscriptions
import sys

def monkey_patch():
    """
    Necessary updates to mailman3 classes and modules to provide
    unified interface to uwtheme's multi-instance
    mailman3 configuration.
    """

    # postorious list view needs to aggregate lists from
    # all mailman3 instances
    list_module = sys.modules.get("postorius.views.list")
    if not list_module:
        from postorius.views import list as list_module

    # replace entire view so we can update block that collects lists using
    # mailman_client.find_lists() with aggregating collector
    setattr(list_module, "list_index_authenticated", list_index_authenticated)

    # replace list_index view with one that has inner function to
    # aggregate lists
    setattr(list_module, "list_index", list_index)

    # get_subscriptions needs to aggregate user subscriptions across
    # all mailman3 instances
    mailman_module = sys.modules.get("django_mailman3.lib.mailman")
    if not mailman_module:
        from django_mailman3.lib import mailman as mailman_module

    # replace get_subscriptions with aggregating collector
    setattr(mailman_module, "get_subscriptions", get_subscriptions)
