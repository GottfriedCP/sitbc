from django.core.management.base import BaseCommand

from decouple import config

import mysql.connector

import os


class Command(BaseCommand):
    help = "Populate g sheet and own DB from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Connect to the NL database
        cnx = mysql.connector.connect(
            user=config("MY_USER"),
            password=config("MY_PASS"),
            host=config("MY_HOST"),
            database="dhsampel",
        )

        # Create a cursor object
        cursor = cnx.cursor()

        for table in (
            "cases",
            "cspro_jobs",
            "cspro_meta",
            "dhsampel_rec",
            "level-1",
            "notes",
        ):
            query = "TRUNCATE TABLE %s"
            cursor.execute(query, (table, ))
            cnx.commit()

        cursor.close()
        cnx.close()

        self.stdout.write(f"berhasil truncate dan buat ulang tabel blob")
        # os.system("/usr/bin/php7.4 /home/gp/htdocs/csweb/ivtb/bin/console csweb:process-cases")
