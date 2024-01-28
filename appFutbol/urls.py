from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    # Consulta sencilla a modelo principal
    path("partidos_api", views.partidos_lista, name="partidos_lista"),
    # Consulta mejorada
    path("partidos_api/mejorada", views.partidos_api_mejorada, name="partidos_api_mejorada"),
    path("recintos/busqueda_recinto", views.recinto_buscar_simple, name="recinto_buscar_simple"),
    path("recintos/busqueda_avanzada", views.recinto_busqueda_avanzada, name="recinto_busqueda_avanzada")
]