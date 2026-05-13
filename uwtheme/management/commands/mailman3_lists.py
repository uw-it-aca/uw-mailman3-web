# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from mailmanclient import Client
import os
import sys
import logging


logging.getLogger().setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'list mailman lists on core server'

    REST_URL = os.getenv('MAILMAN_REST_URL')
    REST_ADMIN = os.getenv('MAILMAN_REST_USER')
    REST_PASSWORD = os.getenv('MAILMAN_REST_PASSWORD')
    REST_API = '3.1'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u', '--url', type=str, default=self.REST_URL,
            help=f"mailman3 server URL, e.g. http://{self.REST_URL}"
        )

        parser.add_argument(
            '-a', '--api', type=str, default=self.REST_API,
            help=f"mailman3 api (default: {self.REST_API})")

    def handle(self, *args, **options):
        mailman3_api_url = options['url']
        mailman3_api = options['api']
        client = Client(f"{mailman3_api_url}/{mailman3_api}",
                        self.REST_ADMIN, self.REST_PASSWORD)
        for mlist in client.get_lists():
            print(mlist.fqdn_listname, file=sys.stdout)
