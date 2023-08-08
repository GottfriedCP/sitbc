from sitbc.models import Faskes

import csv

existing_faskes = Faskes.objects.all()
existing_faskes.delete()

with open("dsfk.csv", "r") as file:
    n = 0
    csv_reader = csv.reader(file, delimiter=";", quotechar='"')
    for line in csv_reader:
        line_exploded = line
        # handle BOM marker on first row
        id_faskes = line_exploded[0][3:] if n == 0 else line_exploded[0]
        # handle newline on last row
        keterangan = (
            line_exploded[-1][:-1]
            if line_exploded[-1].endswith("\n")
            else line_exploded[-1]
        )
        # print(line_exploded)
        faskes = Faskes(
            id_faskes=id_faskes,
            kd_prov=line_exploded[1],
            provinsi=line_exploded[2],
            kode_kk=line_exploded[3],
            kode_prov_kk=line_exploded[4],
            kab_kota=line_exploded[5],
            kode_jenis_faskes=line_exploded[6],
            jenis_faskes=line_exploded[7],
            no_urut=line_exploded[8],
            nama_faskes=line_exploded[9],
            alamat=line_exploded[10],
            telepon=line_exploded[11],
            nama_cp=line_exploded[12],
            no_hp=line_exploded[13],
            keterangan=keterangan,
        )
        # if len(faskes.id_faskes) != 8:
            # print(faskes.id_faskes)
        print(faskes)
        faskes.save()
        n += 1
        # if n == 2:
            # break
