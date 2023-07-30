from django.urls import path

from . import views

app_name = "sitbc"
urlpatterns = [path("", views.index, name="index")]
