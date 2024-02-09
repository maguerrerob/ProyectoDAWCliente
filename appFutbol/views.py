from django.shortcuts import render, redirect
from django.db.models import Q, Prefetch, Count, F,Avg
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from requests.exceptions import HTTPError
from pathlib import Path
import json
from requests.exceptions import HTTPError
import requests
import os
import environ
from pathlib import Path
import xml.etree.ElementTree as ET


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

# Create your views here.

def index(request):
    return render(request, "index.html")

# Para parseado de xml
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    # Procesa el árbol XML según tus necesidades
    return root

def manejar_respuesta(response):
    content_type = response.headers['Content-Type']

    if 'application/json' in content_type:
        return response.json()
    elif 'application/xml' in content_type:
        return parse_xml(response.content)
    else:
        raise ValueError('Formato de respuesta no soportado')


# Consulta sencilla a modelo principal
def partidos_lista(request):
    # Token cliente
    headers = crear_cabecera_cliente()
    
    # Obtenemos todos los partidos
    response = requests.get(env("URL_API") + "partidos", headers=headers)
    
    # Para manejar respuesta json o xml
    partidos = manejar_respuesta(response)

    return render(request, "partidos/partidos_api.html", {"partidos_mostrar": partidos})

# Consulta mejorada
def partidos_api_mejorada(request):
    # Token cliente
    headers = crear_cabecera_cliente()
    response = requests.get(env("URL_API") + "partidos_mejorada", headers=headers)
    partidos = manejar_respuesta(response)
    return render(request, "partidos/partidos_api_mejorada.html", {"partidos_mostrar": partidos})


# Para crear la cabecera, ahí irá los datos de la autenticacion con la API en variables de entorno - clientes
def crear_cabecera_cliente():
    return {'Authorization': 'Bearer '+env("TOKEN_CLIENTE")}

def crear_cabecera_duenyorecinto():
    return {'Authorization': 'Bearer '+env("TOKEN_DUENYORECINTO")}

# Consulta mejorada con autenticación oauth2 en API
def datos_usuario(request):
    headers = crear_cabecera_cliente()
    response = requests.get(env("URL_API") + "datosusuarios", headers=headers)
    datosusuarios = manejar_respuesta(response)
    return render(request, "datosusuario/datosusuario_api.html", {"datos_mostrar":datosusuarios})


def recintos_lista_api(request):
    headers = crear_cabecera_duenyorecinto()
    response = requests.get(env("URL_API") + "recintos/listar", headers=headers)
    recintos = manejar_respuesta(response)
    return render(request, "recintos/listar_recintos_api.html", {"recintos_mostrar":recintos})

# Consulta mejorada con autenticación JWT
def crear_cabecera_jwt():
    return {'Authorization': 'Bearer '+env("TOKEN_JWT")}

def listar_post(request):
    headers = crear_cabecera_jwt()
    response = requests.get(env("URL_API") + "posts/listar", headers=headers)
    posts = manejar_respuesta(response)
    return render(request, "posts/listar_posts_api.html", {"posts_mostrar":posts})


# Búsqueda simple modelo principal
def recinto_buscar_simple(request):
    formulario = BusquedaRecintoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera_duenyorecinto()
        response = requests.get(env("URL_API") + "recintos/busqueda_simple",
            headers=headers,
            params=formulario.cleaned_data
        )
        recintos = manejar_respuesta(response)
        print(recintos)
        return render(request, 'recintos/lista_mejorada_api.html',{"recintos_mostrar":recintos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
# Búsqueda avanzada modelo principal
def recinto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaRecintoForm(request.GET)
        
        try:
            headers = crear_cabecera_duenyorecinto()
            response = requests.get(env("URL_API") + "recintos/busqueda_avanzada",
                headers=headers,
                params=formulario.data
            )
            if(response.status_code == requests.codes.ok):
                recintos = manejar_respuesta(response)
                print(recintos)
                return render(request, 'recintos/lista_mejorada_api.html',
                              {"recintos_mostrar":recintos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = manejar_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'recintos/form_busqueda_avanzada_api.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaRecintoForm(None)
    return render(request, 'recintos/form_busqueda_avanzada_api.html',{"formulario":formulario})


# Búsqueda avanzada
def datosusuario_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaDatosusuarioForm(request.GET)
        
        try:
            headers = crear_cabecera_cliente()
            response = requests.get(env("URL_API") + "datosusuario/busqueda_avanzada",
                headers=headers,
                params=formulario.data
            )
            if(response.status_code == requests.codes.ok):
                datosusuario = manejar_respuesta(response)
                print(datosusuario)
                return render(request, 'datosusuario/datosusuario_api.html',
                              {"datos_mostrar":datosusuario})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = manejar_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'datosusuario/form_busqueda_avanzada_api.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaDatosusuarioForm(None)
    return render(request, 'datosusuario/form_busqueda_avanzada_api.html',{"formulario":formulario})


# Búsqueda avanzada
def partido_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPartidoForm(request.GET)
        
        try:
            headers = crear_cabecera_cliente()
            response = requests.get(env("URL_API") + "partidos/busqueda_avanzada",
                headers=headers,
                params=formulario.data
            )
            if(response.status_code == requests.codes.ok):
                partidos = manejar_respuesta(response)
                print(partidos)
                return render(request, 'partidos/partidos_api_mejorada.html',
                              {"partidos_mostrar":partidos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = manejar_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'partidos/form_busqueda_avanzada_api.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaPartidoForm(None)
    return render(request, 'partidos/form_busqueda_avanzada_api.html',{"formulario":formulario})


def partido_create(request):
    if (request.method == "POST"):
        try:
            formulario = PartidoForm(request.POST)
            headers =  {'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json"}
            datos = formulario.data.copy()
            
            response = requests.post(env("URL_API") + "partido/crear",
                headers=headers,
                data=json.dumps(datos)
            )
            print(response)
            if(response.status_code == requests.codes.ok):
                return redirect("partidos_api_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = manejar_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'partidos/create_api.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = PartidoForm(None)
    return render(request, 'partidos/create_api.html',{"formulario":formulario})


def partido_obtener(request,partido_id):
    partido = helper.obtener_partido(partido_id)
    return render(request, 'partidos/partido_mostrar_api.html',{"partido":partido})


def partido_editar(request, partido_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    partido = helper.obtener_partido(partido_id)
    formulario = PartidoForm(datosFormulario, initial={
        "hora": partido["hora"],
        "estado": partido["estado"],
        "tipo": partido["tipo"],
        "estilo": partido["estilo"],
        "creador": partido["creador"]["id"],
        "campo_reservador": partido["campo_reservado"]["id"]
    })

    if (request.method == "POST"):
        try:
            formulario = PartidoForm(request.POST)
            headers = {'Authorization': 'Bearer '+env("TOKEN_CLIENTE"), "Content-Type": "application/json"}
            datos = request.POST.copy()
            response = requests.put(env("URL_API") + "partido/editar/" + str(partido_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("partido_mostrar_api",partido_id=partido_id)
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'partidos/PUT_api.html',
                            {"formulario":formulario,"partido":partido})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    return render(request, 'partidos/PUT_api.html',{"formulario":formulario,"partido":partido})

# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)