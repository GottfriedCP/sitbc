from django.core.management.base import BaseCommand

import mysql.connector

import os


class Command(BaseCommand):
    help = "Populate g sheet and own DB from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        os.system("/usr/bin/php7.4 /home/gp/htdocs/csweb/ivtb/bin/console csweb:process-cases")
