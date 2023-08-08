from django.shortcuts import render

from .models import Faskes

import random
import urllib.parse


def index(request):
    base_survey_url = "http://bkpk.ddns.net/limesurvey/index.php/415764?lang=id&"
    survey_url = base_survey_url
    params = {}
    faskes = None
    faskes_missing = False
    error_msg = ""
    notify_for_no_id = ""
    if request.method == "POST":
        id_faskes = request.POST.get("id_faskes")
        chall_ans = request.POST.get("chall_ans")
        id_none = request.POST.get("id_none", "")
        try:
            assert int(chall_ans) == request.session.get(
                "challenge_answer", 0
            ), f"Jawaban pertanyaan pengaman tidak cocok."
            if not id_none:
                faskes = Faskes.objects.get(id_faskes=id_faskes)
                params = {
                    "PROV": faskes.kd_prov,
                    "KABKOTA": faskes.kode_prov_kk,
                    "ALMT": str(faskes.alamat).upper(),
                    "NOF": faskes.no_urut,
                    "NMF": str(faskes.nama_faskes).upper(),
                    "TELP": faskes.telepon,
                    "JENISF": faskes.kode_jenis_faskes,
                    "P250A": str(faskes.nama_cp).upper(),
                    "P250B": faskes.no_hp,
                    "CAT": str(faskes.keterangan).upper() if faskes.keterangan else "",
                    "newtest": "Y",
                }
                params_url_encoded = urllib.parse.urlencode(params)
                survey_url = f"{survey_url}{params_url_encoded}"
            else:
                notify_for_no_id = "ID Faskes belum tersedia di sistem. Mohon isi kuesioner kosong"
        except Exception as e:
            faskes_missing = True
            error_msg = e

    # kode pengaman
    op1 = random.randint(1, 99)
    op2 = random.randint(1, 10)
    res = op1 + op2
    request.session["challenge_answer"] = res

    return render(
        request,
        "sitbc/index.html",
        {
            "faskes": faskes,
            "faskes_missing": faskes_missing,
            "error_msg": error_msg,
            "op1": op1,
            "op2": op2,
            "survey_url": survey_url,
            "base_survey_url": base_survey_url,
            "notify_for_no_id": notify_for_no_id,
        },
    )
