from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    # Consulta sencilla a modelo principal
    path("partidos_api", views.partidos_lista, name="partidos_lista"),
    # Consulta mejorada
    path("partidos_api/mejorada", views.partidos_api_mejorada, name="partidos_api_mejorada"),
    path("datosusuarios", views.datos_usuario, name="datos_usuario"),
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
    # PATCH
    path("partido/editar/hora/<int:partido_id>", views.partido_patch_hora, name="partido_patch_hora"),
    # Delete
    path("partido/eliminar/<int:partido_id>", views.partido_eliminar, name="partido_eliminar"),
    # CRUD Recinto
    # Create
    path("recinto/create", views.recinto_create, name="recinto_create"),
    path('recinto/<int:recinto_id>',views.recinto_obtener,name='recinto_obtener'),
    # PUT
    path("recinto/editar/<int:recinto_id>", views.recinto_put, name="recinto_put"),
    # PATCH
    path("recinto/editar_nombre/<int:recinto_id>", views.recinto_patch_nombre, name="recinto_patch_nombre"),
    # Delete
    path("recinto/eliminar/<int:recinto_id>", views.recinto_eliminar, name="recinto_eliminar"),
    # CRUD Datosusuario
    # Create
    path("datosusuario/create", views.datosusuario_create, name="datosusuario_create"),
    # PUT
    path("datosusuario/editar/<int:datosusuario_id>", views.datosusuario_put, name="datosusuario_put"),
    # PATCH
    path("datosusuario/editar_ubicacion/<int:datosusuario_id>", views.datosusuario_ubicacion, name="datosusuario_ubicacion"),
    # Delete
    path("datosusuario/eliminar/<int:datosusuario_id>", views.datosusuario_eliminar, name="datosusuario_eliminar"),
    # Gestión de accesos
    path("registrar", views.registrar_usuario, name="registrar_usuario"),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    # FUNCIONALIDADES
    #Gabi
    path("anyadir_jugador/<int:partido_id>", views.añadir_jugador_partido, name="añadir_jugador_partido"),
    #Irene
    path("anyadir_resultado_partido/<int:partido_id>", views.anyadir_resultado_partido, name="anyadir_resultado_partido"),
    #Alberto
    path("recintos/lista", views.recintos_lista_api, name="recintos_lista_api"),
    #Luis
    path("añadir_amigo/<int:datosusuario_id>", views.sistema_amigos, name="sistema_amigos")
]