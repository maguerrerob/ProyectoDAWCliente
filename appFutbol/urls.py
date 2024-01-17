from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("partidos_api", views.partidos_lista, name="partidos_lista")
]