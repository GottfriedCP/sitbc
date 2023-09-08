from decouple import config
import datetime
import mysql.connector
import numpy as np
import pandas as pd
import pygsheets
import simplejson as json


def pop_ind_nl(self_command):
    gc = pygsheets.authorize(service_account_file="creds.json")
    sheet = gc.open("INDV DATA")

    # Connect to the NL database
    cnx = mysql.connector.connect(
        user=config("MY_USER"),
        password=config("MY_PASS"),
        host=config("MY_HOST"),
        database="sivtbc_ind_nl",
    )

    # Create a cursor object
    cursor = cnx.cursor()

    query = (
        "SELECT l.*, r.* "
        "FROM `ind_nl_rec` as r "
        "INNER JOIN `level-1` as l "
        "ON l.`level-1-id` = r.`level-1-id` "
        "INNER JOIN `cases` as c "
        "ON l.`case-id` = c.`id` "
        "WHERE c.deleted = 0 and c.partial_save_mode IS NULL "
    )

    cursor.execute(query)

    # Fetch the result
    rows = cursor.fetchall()
    number_of_rows = len(rows)
    self_command.stdout.write(f"number of rows: {number_of_rows}")

    if number_of_rows == 0:
        self_command.stdout.write(f"nothing to write")
    else:
        df = pd.DataFrame(rows)
        df.columns = [
            "level-1-id",
            "case-id",
            "b2r1_f",
            "b2r2_f",
            "b2r3_f",
            "b3r1",
            "ind_nl_rec-id",
            "level-1-id",
            "idsampel1",
            "kab",
            "id_ind_nl",
            "device",
            "userid",
            "bcode",
            "rev_nl",
            "b1ar1",
            "b1ar2",
            "b1ar3",
            "no_enum",
            "telp_enum",
            "b1br1",
            "b1br2",
            "dsfk",
            "b2r1",
            "pteks",
            "b2r2",
            "kbteks",
            "b2r3",
            "b2r4",
            "b2r5",
            "kab2",
            "b2r1_b",
            "pteks_b",
            "b2r2_b",
            "kbteks_b",
            "b2r3_b",
            "b2r4_b",
            "b2r5_b",
            "pteks_f",
            "kbteks_f",
            "b2r4_f",
            "b2r5_f",
            "b3r2",
            "b3r3",
            "b3r4",
            "b3r5",
            "b3r6",
            "b3r7",
            "kab1",
            "b3r8a",
            "pteks8",
            "b3r8b",
            "kbteks8",
            "b3r8c",
            "b3r8d",
            "b3r8e",
            "b3r8f",
            "b3r8g",
            "b3r9",
            "b3r9s",
            "b3r10",
            "b3r10s",
            "b4",
            "b4ar1k3",
            "b4ar1k4",
            "b4ar2k3",
            "b4ar2k3s",
            "b4ar2k4",
            "b4ar3k3",
            "b4ar3k4",
            "b4br1k3",
            "b4br1k4",
            "b4br2k3",
            "b4br2k4",
            "b4br3k3",
            "b4br3k4",
            "b4br4k3",
            "b4br4k4",
            "b4br5k3",
            "b4br5k4",
            "b4br6k3",
            "b4br6k4",
            "b4br7k3",
            "b4br7k3s",
            "b4br7k4",
            "b4cr1",
            "b5r1",
            "b5r1s",
            "b5r2",
            "b5r3",
            "b5r4",
            "b5r5a",
            "b5r5a_tgl",
            "b5r5b",
            "b5r5c",
            "b5r5d",
            "b5r6",
            "b5r7a",
            "b5r7b",
            "b5r7c",
            "b5r7d",
            "b5r7e",
            "b5r7f",
            "b5r7g",
            "b5r7h",
            "b5r7i",
            "b5r7j",
            "b5r7k",
            "b5r7l",
            "b5r7m",
            "b5r7n",
            "b5r7o",
            "b5r7p",
            "b5r7q",
            "b5r7r",
            "b5r7s",
            "b5r7t",
            "cat_inl",
        ]
        df = df.replace({np.nan: None})
        worksheet = sheet.worksheet(property="title", value="IND_NL")
        worksheet.clear(start="A1", end=None, fields="*")
        worksheet.set_dataframe(df, (1, 1))

    cursor.close()
    cnx.close()
    # self.stdout.write(f"berhasil menyimpan kabkota {kabkota.kode} {kabkota.nama}")

    today_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    self_command.stdout.write(f"berhasil menulis ke gsheets pada {today_date}")


def pop_ind_l(self_command):
    gc = pygsheets.authorize(service_account_file="creds.json")
    sheet = gc.open("INDV DATA")

    # Connect to the NL database
    cnx = mysql.connector.connect(
        user=config("MY_USER"),
        password=config("MY_PASS"),
        host=config("MY_HOST"),
        database="sivtbc_ind_l",
    )

    # Create a cursor object
    cursor = cnx.cursor()

    query = (
        "SELECT l.*, r.* "
        "FROM `ind_nl_rec` as r "
        "INNER JOIN `level-1` as l "
        "ON l.`level-1-id` = r.`level-1-id` "
        "INNER JOIN `cases` as c "
        "ON l.`case-id` = c.`id` "
        "WHERE c.deleted = 0 and c.partial_save_mode IS NULL "
    )

    cursor.execute(query)

    # Fetch the result
    rows = cursor.fetchall()
    number_of_rows = len(rows)
    self_command.stdout.write(f"number of rows: {number_of_rows}")

    if number_of_rows == 0:
        self_command.stdout.write(f"nothing to write")
    else:
        df = pd.DataFrame(rows)
        df.columns = [
            "level-1-id",
            "case-id",
            "b2r1_f",
            "b2r2_f",
            "b2r3_f",
            "b3r1",
            "ind_nl_rec-id",
            "level-1-id",
            "idsampel1",
            "kab",
            "id_ind_l",
            "rev_l",
            "device",
            "userid",
            "bcode",
            "b1ar1",
            "b1ar2",
            "b1ar3",
            "no_enum",
            "telp_enum",
            "b1br1",
            "b1br2",
            "dsfk",
            "b2r1",
            "pteks",
            "b2r2",
            "kbteks",
            "b2r3",
            "b2r4",
            "b2r5",
            "kab2",
            "b2r1_b",
            "pteks_b",
            "b2r2_b",
            "kbteks_b",
            "b2r3_b",
            "b2r4_b",
            "b2r5_b",
            "pteks_f",
            "kbteks_f",
            "b2r4_f",
            "b2r5_f",
            "b3r2",
            "b3r3",
            "b3r4",
            "b3r5",
            "b3r6",
            "b3r7",
            "b3r8",
            "kab1",
            "b3r9a",
            "pteks9",
            "b3r9b",
            "kbteks9",
            "b3r9c",
            "b3r9d",
            "b3r9e",
            "b3r9f",
            "b3r9g",
            "b3r10",
            "b4r1k3",
            "b4r1k4",
            "b4r2k3",
            "b4r2k4",
            "b4r3k3",
            "b4r3k4",
            "b4r4k3",
            "b4r4k4",
            "b4r5k3",
            "b4r5k4",
            "b4r6k3",
            "b4r6k4",
            "b4r7k3",
            "b4br7k3s",
            "b4r7k4",
            "b4r8k3",
            "b4r8k4",
            "cat_il",
        ]
        df = df.replace({np.nan: None})
        worksheet = sheet.worksheet(property="title", value="IND_L")
        worksheet.clear(start="A1", end=None, fields="*")
        worksheet.set_dataframe(df, (1, 1))

    cursor.close()
    cnx.close()
    # self.stdout.write(f"berhasil menyimpan kabkota {kabkota.kode} {kabkota.nama}")

    today_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    self_command.stdout.write(f"berhasil menulis ke gsheets pada {today_date}")
