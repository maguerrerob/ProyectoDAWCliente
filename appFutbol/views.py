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

import requests
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Create your views here.

def index(request):
    return render(request, "index.html")


# Consulta sencilla a modelo principal
def partidos_lista(request):
    # Token cliente
    headers = crear_cabecera_cliente()
    
    # Obtenemos todos los partidos
    response = requests.get("http://127.0.0.1:8000/api/v1/partidos", headers=headers)
    
    # Transformamos la respuesta en json
    partidos = response.json()
    return render(request, "partidos/partidos_api.html", {"partidos_mostrar": partidos})

# Consulta mejorada
def partidos_api_mejorada(request):
    # Token cliente
    headers = crear_cabecera_cliente()

    response = requests.get("http://127.0.0.1:8000/api/v1/partidos_mejorada", headers=headers)

    partidos = response.json()
    return render(request, "partidos/partidos_api_mejorada.html", {"partidos_mostrar": partidos})


# Para crear la cabecera, ahí irá los datos de la autenticacion con la API en variables de entorno - clientes
def crear_cabecera_cliente():
    return {'Authorization': 'Bearer '+env("TOKEN_CLIENTE")}

def crear_cabecera_duenyorecinto():
    return {'Authorization': 'Bearer '+env("TOKEN_DUENYORECINTO")}

# Consulta mejorada con autenticación oauth2 en API
def datos_usuario(request):
    headers = crear_cabecera_cliente()
    response = requests.get("http://127.0.0.1:8000/api/v1/datosusuarios", headers=headers)
    datosusuarios = response.json()
    return render(request, "datosusuario/datosusuario_api.html", {"datos_mostrar":datosusuarios})


def recintos_lista_api(request):
    headers = crear_cabecera_duenyorecinto()
    response = requests.get("http://127.0.0.1:8000/api/v1/recintos/listar", headers=headers)
    recintos = response.json()
    return render(request, "recintos/listar_recintos_api.html", {"recintos_mostrar":recintos})

# Consulta mejorada con autenticación JWT
def crear_cabecera_jwt():
    return {'Authorization': 'Bearer '+env("TOKEN_JWT")}

def listar_post(request):
    headers = crear_cabecera_jwt()
    response = requests.get("http://127.0.0.1:8000/api/v1/posts/listar", headers=headers)
    posts = response.json()
    return render(request, "posts/listar_posts_api.html", {"posts_mostrar":posts})


def recinto_buscar_simple(request):
    formulario = BusquedaRecintoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera_duenyorecinto()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/recintos/busqueda_simple',
            headers=headers,
            params=formulario.cleaned_data
        )
        recintos = response.json()
        print(recintos)
        return render(request, 'recintos/lista_mejorada_api.html',{"recintos_mostrar":recintos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    

def recinto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaRecintoForm(request.GET)
        
        try:
            headers = crear_cabecera_cliente()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/recintos/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            if(response.status_code == requests.codes.ok):
                recintos = response.json()
                print(recintos)
                return render(request, 'recintos/lista_mejorada_api.html',
                              {"recintos_mostrar":recintos})
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
                            'recintos/lista_mejorada_api.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaRecintoForm(None)
    return render(request, 'recintos/form_busqueda_avanzada_api.html',{"formulario":formulario})


def partido_create(request):
    if (request.method == "POST"):
        try:
            formulario = PartidoForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_CLIENTE"), "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            # Para campos que son varios valores de selección
            datos["usuarios_jugadores"] = request.POST.getlist("usuarios_jugadores");
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/partido/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("partidos_api_mejorada")
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


# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)