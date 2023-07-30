from django.db import models


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
