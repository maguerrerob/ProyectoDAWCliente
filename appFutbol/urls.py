from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    # Consulta sencilla a modelo principal
    path("partidos_api", views.partidos_lista, name="partidos_lista"),
    # Consulta mejorada
    path("partidos_api/mejorada", views.partidos_api_mejorada, name="partidos_api_mejorada"),
    path("datosusuarios", views.datos_usuario, name="datos_usuario"),
    path("recintos/lista", views.recintos_lista_api, name="recintos_lista_api"),
    # Consulta mejorada con JWT
    path("posts/listar", views.listar_post, name="listar_post"),
    path("recintos/busqueda_recinto", views.recinto_buscar_simple, name="recinto_buscar_simple"),
    path("recintos/busqueda_avanzada", views.recinto_busqueda_avanzada, name="recinto_busqueda_avanzada"),
    path("datosusuario/busqueda_avanzada", views.datosusuario_busqueda_avanzada, name="datosusuario_busqueda_avanzada"),
    path("partidos/busqueda_avanzada/", views.partido_busqueda_avanzada, name="partido_busqueda_avanzada"),
    path("partido/obtener/<int:partido_id>", views.partido_obtener, name="partido_obtener"),
    # CRUD Partido
    # Create
    path("partido/create", views.partido_create, name="partido_create"),
    # PUT
    path("partido/put/<int:partido_id>", views.partido_put, name="partido_put"),
    # Delete
    path("partido/eliminar/<int:partido_id>", views.partido_eliminar, name="partido_eliminar"),
    # CRUD Recinto
    # Create
    path("recinto/create", views.recinto_create, name="recinto_create"),
    path('recinto/<int:recinto_id>',views.recinto_obtener,name='recinto_obtener'),
    # PUT
    path("recinto/editar/<int:recinto_id>", views.recinto_put, name="recinto_put"),
    # Delete
    path("recinto/eliminar/<int:recinto_id>", views.recinto_eliminar, name="recinto_eliminar"),
    # CRUD Datosusuario
    # Create
    path("datosusuario/create", views.datosusuario_create, name="datosusuario_create"),
    # PUT
    path("datosusuario/editar/<int:datosusuario_id>", views.datosusuario_put, name="datosusuario_put"),
    # Delete
    path("datosusuario/eliminar/<int:datosusuario_id>", views.datosusuario_eliminar, name="datosusuario_eliminar")
]