from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("partidos_api", views.partidos_lista, name="partidos_lista"),
    path("recintos/busqueda_recinto", views.recinto_buscar_simple, name="recinto_buscar_simple"),
    path("recintos/busqueda_avanzada", views.recinto_busqueda_avanzada, name="recinto_busqueda_avanzada")
]