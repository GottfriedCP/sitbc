from django.urls import include, path

from . import views

app_name = "sitbc"
urlpatterns = [
    path("", views.index, name="index"),
    path("dasbor/", include("sitbc.dasbor.urls", namespace="dasbor")),
]
