from django.shortcuts import render, redirect
from django.db.models import Q, Prefetch, Count, F,Avg
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
import requests
from  django.core import serializers

# Create your views here.

def index(request):
    return render(request, "index.html")

# Para crear la cabecera, ahí irá los datos de la autenticacion con la API
def crear_cabecera():
    return {'Authorization': 'Bearer UaAG1imxXEmX90JSlVG8YMQ89Lwiet'}

def partidos_lista(request):
    # Token cliente
    headers = {"Authorization":"Bearer UaAG1imxXEmX90JSlVG8YMQ89Lwiet"}
    
    # Obtenemos todos los partidos
    response = requests.get("http://127.0.0.1:8000/api/v1/partidos", headers=headers)
    
    # Transformamos la respuesta en json
    partidos = response.json()
    return render(request, "partidos/partidos_api.html", {"partidos_mostrar": partidos})

def recinto_buscar_simple(request):
    formulario = BusquedaRecintoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
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
    
from requests.exceptions import HTTPError