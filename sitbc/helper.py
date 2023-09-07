from decouple import config
import datetime
import mysql.connector
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
        "FROM `level-1` as l "
        "INNER JOIN `ind_nl_rec` as r "
        "ON l.`level-1-id` = r.`level-1-id` "
    )

    cursor.execute(query)

    # Fetch the result
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    self_command.stdout.write(f"number of rows: {len(rows)}")

    worksheet = sheet.worksheet(property="title", value="IND_NL")

    worksheet.set_dataframe(df, (2, 1))

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
        "FROM `level-1` as l "
        "INNER JOIN `ind_nl_rec` as r "
        "ON l.`level-1-id` = r.`level-1-id` "
    )

    cursor.execute(query)

    # Fetch the result
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    self_command.stdout.write(f"number of rows: {len(rows)}")

    worksheet = sheet.worksheet(property="title", value="IND_L")
    worksheet.set_dataframe(df, (2, 1))

    cursor.close()
    cnx.close()
    # self.stdout.write(f"berhasil menyimpan kabkota {kabkota.kode} {kabkota.nama}")

    today_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    self_command.stdout.write(f"berhasil menulis ke gsheets pada {today_date}")
