from django.core.management.base import BaseCommand
from django.db.models import F

import datetime

from decouple import config

import mysql.connector

from sitbc.models import Individu, KabupatenKota


class Command(BaseCommand):
    help = "Populate g sheet and own DB from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # populate g sheets
        # pop_ind_nl(self)
        # pop_ind_l(self)

        Individu.objects.all().delete()
        kks = KabupatenKota.objects.all()
        for kk in kks:
            kk.reset_jml()
            kk.save()
        # Connect to the NL database
        n = 0
        for db_name in ("sivtbc_ind_nl", "sivtbc_ind_l"):
            cnx = mysql.connector.connect(
                user=config("MY_USER"),
                password=config("MY_PASS"),
                host=config("MY_HOST"),
                database=db_name,
            )

            # Create a cursor object
            cursor = cnx.cursor()

            if n == 0:
                query = (
                    "SELECT l.b2r1_f as kode_prov, l.b2r2_f as kode_kab, "
                    "r.pteks_f as nama_prov, r.kbteks_f as nama_kab, "
                    "r.dsfk as dsfk, "
                    "l.b2r3_f as nu_faskes, r.b2r5_f as jenis_faskes, "
                    "r.b2r4_f as nama_faskes, "
                    "l.b3r1 as nu_ind, r.b3r3 as nama, r.b3r4 as jk, "
                    "r.b1br1 as nama_enum, r.telp_enum as telp_enum, r.b1br2 as tgl_kunjungan "
                    "FROM `level-1` as l "
                    "INNER JOIN `ind_nl_rec` as r "
                    "ON l.`level-1-id` = r.`level-1-id`"
                )
            else:
                query = (
                    "SELECT l.b2r1_f as kode_prov, l.b2r2_f as kode_kab, "
                    "r.pteks_f as nama_prov, r.kbteks_f as nama_kab, "
                    "r.dsfk as dsfk, "
                    "l.b2r3_f as nu_faskes, r.b2r5_f as jenis_faskes, "
                    "r.b2r4_f as nama_faskes, "
                    "l.b3r1 as nu_ind, r.b3r4 as nama, r.b3r5 as jk, "
                    "r.b1br1 as nama_enum, r.telp_enum as telp_enum, r.b1br2 as tgl_kunjungan "
                    "FROM `level-1` as l "
                    "INNER JOIN `ind_nl_rec` as r "
                    "ON l.`level-1-id` = r.`level-1-id`"
                )

            cursor.execute(query)

            # Fetch the result
            rows = cursor.fetchall()
            for row in rows:
                indiv = Individu(
                    kode_prov=row[0],
                    kode_kab=row[1],
                    nama_prov=str(row[2]).upper(),
                    nama_kab=str(row[3]).upper(),
                    dsfk=row[4],
                    nu_faskes=row[5],
                    jenis_faskes=row[6],
                    nama_faskes=str(row[7]).upper(),
                    nu_ind=row[8],
                    nama=str(row[9]).upper(),
                    jk=row[10],
                    nama_enum=str(row[11]).upper(),
                    telp_enum=row[12],
                    tgl_kunjungan=row[13],
                )
                indiv.save()

                kk = (
                    KabupatenKota.objects.get(kode=indiv.kode_prov_kab)
                    if KabupatenKota.objects.filter(kode=indiv.kode_prov_kab).exists()
                    else None
                )
                if kk:
                    kk.jml_indiv = F("jml_indiv") + 1
                    jenis_faskes = int(indiv.jenis_faskes) if indiv.jenis_faskes else 9
                    if jenis_faskes == 1:
                        kk.jml_rs = F("jml_rs") + 1
                    elif jenis_faskes == 2:
                        kk.jml_pkm = F("jml_pkm") + 1
                    elif jenis_faskes == 3:
                        kk.jml_klinik = F("jml_klinik") + 1
                    elif jenis_faskes == 4:
                        kk.jml_dpm = F("jml_dpm") + 1
                    elif jenis_faskes == 5:
                        kk.jml_balai = F("jml_balai") + 1
                    elif jenis_faskes == 6:
                        kk.jml_lab = F("jml_lab") + 1
                    kk.save()

            cursor.close()
            cnx.close()
            n += 1

        today_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.stdout.write(f"berhasil menulis ke gsheets dan DB pada {today_date}")
