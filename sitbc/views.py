from django.shortcuts import render

from .models import Faskes

import random
import urllib.parse


def index(request):
    survey_url = "https://pusjakuk2.ddns.net/limesurvey/index.php/535678?lang=id&"
    params = {}
    faskes = None
    faskes_missing = False
    error_msg = ""
    if request.method == "POST":
        id_faskes = request.POST.get("id_faskes")
        chall_ans = request.POST.get("chall_ans")
        try:
            assert int(chall_ans) == request.session.get(
                "challenge_answer", 0
            ), f"Jawaban pertanyaan pengaman tidak cocok."
            faskes = Faskes.objects.get(id_faskes=id_faskes)
            params = {
                "PROV": faskes.kd_prov,
                "KABKOTA": faskes.kode_prov_kk,
                "ALMT": faskes.alamat,
                "NOF": faskes.no_urut,
                "NMF": faskes.nama_faskes,
                "TELP": faskes.telepon,
                "JENISF": faskes.kode_jenis_faskes,
                "P250A": faskes.nama_cp,
                "P250B": faskes.no_hp,
                "CAT": faskes.keterangan if faskes.keterangan else "",
                "newtest": "Y",
            }
            params_url_encoded = urllib.parse.urlencode(params)
            survey_url = f"{survey_url}{params_url_encoded}"
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
        },
    )
