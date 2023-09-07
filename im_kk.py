from sitbc.models import KabupatenKota

import csv

with open("kabkota.csv", "r") as file:
    n = 0
    KabupatenKota.objects.all().delete()
    csv_reader = csv.reader(
        file,
        delimiter=",",
    )
    for line in csv_reader:
        kode = line[0][3:] if n == 0 else line[0]
        kode_prov = line[1]
        kode_kab = line[2]
        nama = line[3]
        nama_prov = line[4]
        n += 1

        kk = KabupatenKota(
            kode=kode,
            kode_kab=kode_kab,
            kode_prov=kode_prov,
            nama=nama,
            nama_prov=nama_prov,
        )
        kk.save()
        print(kk.kode)
