from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from sitbc.models import Individu, KabupatenKota


@login_required
def index(request, kode_kab=None):
    kks = KabupatenKota.objects.all().order_by("kode")
    context = {
        "kks": kks,
    }
    return render(request, "dasbor/index.html", context)


@login_required
def detail(request, kode_kab):
    kk = get_object_or_404(KabupatenKota, kode=kode_kab)
    indivs = Individu.objects.filter(kode_prov_kab=kode_kab)
    context = {
        "kk": kk,
        "indivs": indivs,
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
