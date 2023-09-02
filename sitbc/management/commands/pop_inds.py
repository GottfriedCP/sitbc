from django.core.management.base import BaseCommand

from decouple import config
import datetime
import mysql.connector
import pygsheets


class Command(BaseCommand):
    help = "Populate g sheet from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        n = 0
        for db in ("sivtbc_ind_nl", "sivtbc_ind_l"):
            # Connect to the NL database
            cnx = mysql.connector.connect(
                user=config("MY_USER"),
                password=config("MY_PASS"),
                host=config("MY_HOST"),
                database=db,
            )

            # Create a cursor object
            cursor = cnx.cursor()

            query = (
                "SELECT l.*, r.* "
                "FROM `level-1` as l "
                "INNER JOIN `ind_nl_rec` as r "
                "ON l.`level-1-id` = r.`level-1-id` "
            )

            cursor.execute(query)

            # Fetch the result
            rows = cursor.fetchall()
            self.stdout.write(f"number of rows: {len(rows)}")

            gc = pygsheets.authorize(service_account_file="creds.json")
            sh = gc.open("INDV DATA")
            wk = sh[n]

            cursor.close()
            cnx.close()
            n += 1
            # self.stdout.write(f"berhasil menyimpan kabkota {kabkota.kode} {kabkota.nama}")

        today_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.stdout.write(f"berhasil menulis ke gsheets pada {today_date}")
