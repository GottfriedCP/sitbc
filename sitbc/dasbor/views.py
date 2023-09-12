from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from sitbc.models import Individu, KabupatenKota


@login_required
def index(request, kode_kab=None):
    kks = KabupatenKota.objects.all().order_by("kode")
    nas_jml_indiv = 0
    jml_fk_unik_list = []
    for kk in kks:
        jml_fk_unik = (
            Individu.objects.filter(kode_prov_kab=kk.kode)
            .values("nu_faskes", "jenis_faskes")
            .distinct()
            .count()
        )
        nas_jml_indiv += kk.jml_indiv
        jml_fk_unik_list.append(jml_fk_unik)

    # PROD SERVER ONLY
    log_time = ""
    try:
        with open("/home/gp/sitbc/pop_inds.log", "r") as logfile:
            log_time = logfile.read()
    except:
        pass

    context = {
        "kks": zip(kks, jml_fk_unik_list),
        "nas_jml_indiv": nas_jml_indiv,
        "nas_jml_faskes": sum(jml_fk_unik_list),
        "log_time": log_time,
        # untuk grafik
        "indivs_per_kk": [[kk.nama for kk in kks], [kk.jml_indiv for kk in kks]],
    }
    return render(request, "dasbor/index.html", context)


@login_required
def detail(request, kode_kab):
    kk = get_object_or_404(KabupatenKota, kode=kode_kab)
    indivs = (
        Individu.objects.filter(kode_prov_kab=kode_kab)
        .annotate(
            nu_ind_int=Cast("nu_ind", IntegerField()),
            nu_faskes_int=Cast("nu_faskes", IntegerField()),
        )
        .order_by("nu_faskes_int", "nu_ind_int")
    )
    jml_fk_unik = (
        Individu.objects.filter(kode_prov_kab=kk.kode)
        .values("nu_faskes", "jenis_faskes")
        .distinct()
        .count()
    )

    # untuk grafik pie
    data_label = ["RS", "PKM", "Klinik", "DPM", "Balai", "Lab"]
    data_faskes = [
        kk.jml_rs,
        kk.jml_pkm,
        kk.jml_klinik,
        kk.jml_dpm,
        kk.jml_balai,
        kk.jml_lab,
    ]
    valid_pie = sum(data_faskes) > 0

    # PROD SERVER ONLY
    log_time = ""
    try:
        with open("/home/gp/sitbc/pop_inds.log", "r") as logfile:
            log_time = logfile.read()
    except:
        pass

    context = {
        "kk": kk,
        "indivs": indivs,
        "jml_faskes": jml_fk_unik,
        "log_time": log_time,
        "data_proporsi_faskes": [data_label, data_faskes],
        "valid_pie": valid_pie,
    }
    return render(request, "dasbor/detail.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("sitbc:dasbor:index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("sitbc:dasbor:index")

    return render(request, "dasbor/login.html", context={})
