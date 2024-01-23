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
    return render(request, "index2.html")

def partidos_lista(request):
    # Token cliente
    headers = {"Authorization":"Bearer UaAG1imxXEmX90JSlVG8YMQ89Lwiet"}
    
    # Obtenemos todos los partidos
    response = requests.get("http://127.0.0.1:8000/api/v1/partidos", headers=headers)
    
    # Transformamos la respuesta en json
    partidos = response.json()
    return render(request, "partidos/partidos_api.html", {"partidos_mostrar": partidos})

def partido_buscar_simple(request):
    formulario = BusquedaPartidoForm(request.GET)