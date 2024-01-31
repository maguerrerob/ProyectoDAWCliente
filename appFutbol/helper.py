import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:
    def obtener_clientes_select():
        headers = {'Authorization': 'Bearer '+env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/clientes/listar',headers=headers)
        clientes = response.json()
        
        lista_clientes = [("","Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente["id"], cliente["usuario"]["username"]))
        return lista_clientes
    
    def obtener_recintos_select():
        headers = {'Authorization': 'Bearer '+env("TOKEN_CLIENTE")}
        response = requests.get('http://127.0.0.1:8000/api/v1/recintos/listar',headers=headers)
        recintos = response.json()
        
        lista_recintos = []
        for recinto in recintos:
            lista_recintos.append((recinto["id"], recinto["nombre"]))