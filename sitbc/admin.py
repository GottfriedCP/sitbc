from django.contrib import admin
from sitbc.models import KabupatenKota


@admin.register(KabupatenKota)
class KabupatenKotaAdmin(admin.ModelAdmin):
    list_display = (
        "kode",
        "nama",
        "nama_prov",
        "jml_indiv",
        "jml_rs",
        "jml_pkm",
        "jml_klinik",
        "jml_dpm",
        "jml_balai",
        "jml_lab",
    )
