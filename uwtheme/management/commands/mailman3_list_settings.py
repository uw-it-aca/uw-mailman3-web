# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from restclients_core.exceptions import DataFailureException
from argparse import FileType
from mailmanclient import Client
import re
import os
import sys
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Get or set mailman3 list settings'

    REST_URL = os.getenv('MAILMAN_REST_URL')
    REST_ADMIN = os.getenv('MAILMAN_REST_USER')
    REST_PASSWORD = os.getenv('MAILMAN_REST_PASSWORD')
    REST_API = '3.1'

    def add_arguments(self, parser):
        parser.add_argument(
            'lists',
            nargs='?',
            type=FileType('r'),
            default=sys.stdin,
            help='file containing list of list names (default: stdin)'
        )

        parser.add_argument(
            '-u', '--url', type=str, default=self.REST_URL,
            help=f"mailman3 server URL, e.g. http://{self.REST_URL}"
        )

        parser.add_argument(
            '-a','--api', type=str, default=self.REST_API,
            help=f"mailman3 api (default: {self.REST_API})")

        parser.add_argument(
            '-s','--setting', type=str, nargs='*',
            help="specific setting name ('<setting_name>=<value>' to sets)")

        parser.add_argument(
            '-c', '--commit', action='store_true', dest='update_setting',
            default=False,
            help='Commit settings update to list (default only echos change)',
        )

    def handle(self, *args, **options):
        mailman3_api_url = options['url']
        mailman3_api = options['api']
        lists = options['lists']
        settings = options['setting']
        update_setting = options['update_setting']

        client = Client(f"{mailman3_api_url}/{mailman3_api}",
                        self.REST_ADMIN, self.REST_PASSWORD)

        for l in lists:
            list_name = l.strip()
            if list_name:
                mlist = client.get_list(list_name)
                if settings:
                    self.handle_settings(mlist, settings, update_setting)
                else:
                    logger.info(f"{list_name}: {mlist.settings}")

    def handle_settings(self, mlist, settings, update_setting):
        mlist_dirty = False
        for setting in settings:
            if '=' in setting:
                mlist_dirty = True
                key, value = setting.split('=', 1)

                if re.match(r"^\[.*\]$", value):
                    value = value[1:-1].split(',')
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'

                mlist.settings[key] = value
                logger.info(f"{mlist.fqdn_listname}: {'' if update_setting else 'WOULD '}SET {key} = {value}")
            else:
                logger.info(f"{mlist.fqdn_listname}: {setting} = {mlist.settings[setting]}")

        if update_setting and mlist_dirty:
            mlist.save()
