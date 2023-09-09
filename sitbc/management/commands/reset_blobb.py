from django.core.management.base import BaseCommand

from decouple import config

import mysql.connector

import os


class Command(BaseCommand):
    help = "Populate g sheet and own DB from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for db_name in ("sivtbc_ind_nl", "sivtbc_ind_l"):
            # Connect to the NL database
            cnx = mysql.connector.connect(
                user=config("MY_USER"),
                password=config("MY_PASS"),
                host=config("MY_HOST"),
                database=db_name,
            )

            # Create a cursor object
            cursor = cnx.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            for table in (
                "cases",
                "cspro_jobs",
                "cspro_meta",
                "ind_nl_rec",
                "level-1",
                "notes",
            ):
                query = f"TRUNCATE TABLE `{table}`"
                cursor.execute(query)
            
            cnx.commit()
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            cursor.close()
            cnx.close()

        os.system("/usr/bin/php7.4 /home/gp/htdocs/csweb/ivtb/bin/console csweb:process-cases")
        self.stdout.write(f"berhasil truncate dan buat ulang tabel blob")
