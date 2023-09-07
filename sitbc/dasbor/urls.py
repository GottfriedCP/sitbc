from django.urls import path

from . import views

app_name = "sitbc"
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<str:kode_kab>/", views.detail, name="detail"),
    path("login/", views.login_view, name="login"),
]
