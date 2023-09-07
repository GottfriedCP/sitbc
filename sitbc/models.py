from django.db import models

import datetime


class Faskes(models.Model):
    id_faskes = models.CharField(max_length=10, unique=True)
    kd_prov = models.CharField(max_length=5)
    provinsi = models.CharField(max_length=100)
    kode_kk = models.CharField(max_length=5)
    kode_prov_kk = models.CharField(max_length=10)
    kab_kota = models.CharField(max_length=100)
    kode_jenis_faskes = models.CharField(max_length=5)
    jenis_faskes = models.CharField(max_length=50)
    no_urut = models.CharField(max_length=5)
    nama_faskes = models.CharField(max_length=150)
    alamat = models.TextField()
    telepon = models.CharField(max_length=100, null=True, blank=True)
    nama_cp = models.CharField(max_length=150, null=True, blank=True)
    no_hp = models.CharField(max_length=100, null=True, blank=True)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_faskes} {self.nama_faskes}"


class Individu(models.Model):
    """Individu terduga/penderita TB di setiap faskes."""

    kode_prov = models.CharField(max_length=3, null=True, blank=True)
    kode_kab = models.CharField(max_length=3, null=True, blank=True)
    kode_prov_kab = models.CharField(max_length=6, null=True, blank=True)
    nama_prov = models.CharField(max_length=100, null=True, blank=True)
    nama_kab = models.CharField(max_length=100, null=True, blank=True)
    dsfk = models.CharField(max_length=2, null=True, blank=True)
    nu_faskes = models.CharField(max_length=5, null=True, blank=True)
    jenis_faskes = models.CharField(max_length=3, null=True, blank=True)
    nama_faskes = models.CharField(max_length=100, null=True, blank=True)
    nu_ind = models.CharField(max_length=5, null=True, blank=True)
    nama = models.CharField(max_length=100, null=True, blank=True)
    jk = models.CharField(max_length=2, null=True, blank=True)
    nama_enum = models.CharField(max_length=100, null=True, blank=True)
    telp_enum = models.CharField(max_length=20, null=True, blank=True)
    tgl_kunjungan = models.CharField(max_length=50, null=True, blank=True)

    def get_tgl_kunjungan(self):
        tgl_kunjungan = self.tgl_kunjungan
        if len(tgl_kunjungan) < 8:
            tgl_kunjungan = f"0{tgl_kunjungan}"
        return datetime.datetime.strptime(tgl_kunjungan, "%d%m%Y").date()

    def get_jenis_faskes_text(self):
        try:
            jf = int(self.jenis_faskes)
        except:
            jf = 99
        if jf == 1:
            return "RS"
        elif jf == 2:
            return "PKM"
        elif jf == 3:
            return "KLINIK"
        elif jf == 4:
            return "DPM"
        elif jf == 5:
            return "BALAI"
        elif jf == 6:
            return "LAB"
        return "INVALID"

    def get_jk_text(self):
        return "L" if self.jk == "1" else "P"

    def save(self, *args, **kwargs):
        kode_kab = "00"
        if len(str(self.kode_kab)) < 2:
            kode_kab = f"0{self.kode_kab}"
            self.kode_kab = kode_kab
        else:
            kode_kab = self.kode_kab
        self.kode_prov_kab = f"{self.kode_prov}{kode_kab}"
        super().save(*args, **kwargs)


class KabupatenKota(models.Model):
    """Kabupaten/Kota yang terlibat."""

    kode = models.CharField(max_length=5)
    kode_kab = models.CharField(max_length=3)
    kode_prov = models.CharField(max_length=3)
    nama = models.CharField(max_length=100)
    nama_prov = models.CharField(max_length=100)
    jml_indiv = models.IntegerField(default=0)
    jml_rs = models.IntegerField(default=0)
    jml_pkm = models.IntegerField(default=0)
    jml_klinik = models.IntegerField(default=0)
    jml_dpm = models.IntegerField(default=0)
    jml_balai = models.IntegerField(default=0)
    jml_lab = models.IntegerField(default=0)

    def get_jml_faskes(self):
        return (
            self.jml_rs
            + self.jml_pkm
            + self.jml_klinik
            + self.jml_dpm
            + self.jml_balai
            + self.jml_lab
        )

    def reset_jml(self):
        self.jml_indiv = 0
        self.jml_rs = 0
        self.jml_pkm = 0
        self.jml_klinik = 0
        self.jml_dpm = 0
        self.jml_balai = 0
        self.jml_lab = 0
