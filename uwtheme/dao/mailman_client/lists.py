#
#
#

from uwtheme.dao.mailman_client import instance_mailman_clients
from uwtheme.dao.mailman_client.user import get_mailman_user
from urllib.error import HTTPError
import sys
import logging


logger = logging.getLogger(__name__)


def find_all_lists(username, role=None, count=100):
    """Iterative implementation of local function in
     postorius/src/postorius/views/list.py:list_index_authenticated
    """
    lists = []

    for web_host, client in instance_mailman_clients():

        instance_lists = _get_lists_in_instance(client, username, role)

        logger.debug(f"Found {len(instance_lists)} lists on client {client}")

        # add web_host to the MailingList object for template reference
        for mlist in instance_lists:
            logger.debug(f"adding web_host {web_host} to "
                         f"list {mlist.list_id}")
            mlist.web_host = web_host

        lists.extend(instance_lists)

    return lists


def get_all_list_page(count, page, advertised=False):
    page_model = None

    for web_host, client in instance_mailman_clients():
        instance_page = _get_list_page(client, count, page, advertised)
        if instance_page is None:
            continue

        list_count = len(instance_page)

        # augment MailingList objects with web_host for template reference
        for entry in instance_page._entries:
            entry.web_host = web_host

        logger.debug(f"Found {list_count} lists on page "
                     f"{page} from {client}")

        if page_model:
            logger.debug(f"Adding {list_count} lists to page model with "
                         f"{len(page_model)} lists")
            for entry in instance_page._entries:
                page_model._entries.append(entry)

            list_count = len(page_model)
        else:
            page_model = instance_page

        if list_count == count:
                break

        logger.debug(f"Response does not fill page {page} of size {count})")

        # reset page and gather remaining lists to fill out page
        page = 0
        count = count - list_count

    return page_model


def _get_lists_in_instance(client, username, role):
    try:
        mm_user = get_mailman_user(client, username)
        user_id = mm_user.user_id if mm_user else None
        instance_lists = client.find_lists(
            user_id, role=role, mail_host=None, count=sys.maxsize)

        logger.debug(f"found {len(instance_lists)} lists for "
                     f"user {username} ({user_id}) "
                     f"with role {role} in "
                     f"Mailman instance at {client}")

        return instance_lists
    except HTTPError as ex:
        logger.debug(f"No lists found for user_id={user_id}, "
                     f"role={role}, mail_host={client}: "
                     f"{ex}")

    return []


def _get_list_page(client, count, page, advertised=False):
    try:
        logger.debug(f"fetching list page from {client} with "
                     f"count={count}, page={page}")

        page = client.get_list_page(
            count=count, page=page, advertised=advertised)

        logger.debug(f"found {page} lists "
                     f"on Mailman instance at {client}")

        return page
    except HTTPError as ex:
        logger.debug(f"No lists found on instance mail_host={client}: {ex}")

    return None
