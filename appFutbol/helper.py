import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:
    def obtener_clientes_select(request):
        headers = {'Authorization': 'Bearer '+ request.session["token"]}
        response = requests.get(env("URL_API") + "clientes/listar",headers=headers)
        clientes = response.json()
        
        lista_clientes = []
        for cliente in clientes:
            lista_clientes.append((cliente["id"],cliente["usuario"]["username"]))
        return lista_clientes
    
    def obtener_recintos_select(request):
        headers = {'Authorization': 'Bearer '+ request.session["token"]}
        response = requests.get(env("URL_API") + 'recintos/listar',headers=headers)
        recintos = response.json()
        
        lista_recintos = [("", "Selecciona campo")]
        for recinto in recintos:
            lista_recintos.append((recinto["id"], recinto["nombre"]))
        return lista_recintos
    
    def obtener_partido(partido_id, request):
        headers = {'Authorization': 'Bearer '+ request.session["token"],
                        "Content-Type": "application/json"}
        response = requests.get(env("URL_API") + "partido/" + str(partido_id),headers=headers)
        partido = response.json()
        print(partido)
        
        return partido
    
    def obtener_duenyosrecintos_select(request):
        headers = {'Authorization': 'Bearer '+ request.session["token"]}
        response = requests.get(env("URL_API") + "duenyosrecintos/listar",headers=headers)
        duenyosrecintos = response.json()
        print(duenyosrecintos)
        lista_duenyosrecintos =  [("", "Selecciona un campo")]
        for duenyorecinto in duenyosrecintos:
            lista_duenyosrecintos.append((duenyorecinto["id"], duenyorecinto["usuario"]["username"]))
        
        return lista_duenyosrecintos
    
    def obtener_recinto(recinto_id, request):
        headers = {'Authorization': 'Bearer '+ request.session["token"]} 
        response = requests.get(env("URL_API") + "recinto/" + str(recinto_id),headers=headers)
        recinto = response.json()
        return recinto
    
    def obtener_datosusuario(datosusuario_id, request):
        headers = {'Authorization': 'Bearer '+ request.session["token"]}
        response = requests.get(env("URL_API") + "datosusuario/" + str(datosusuario_id),headers=headers)
        datosusuario = response.json()
        return datosusuario
    
    def obtener_token_session(usuario,password):
            token_url = env("URL_OBTENER_TOKEN")
            data = {
                'grant_type': 'password',
                'username': usuario,
                'password': password,
                'client_id': 'client_id',
                'client_secret': 'client_secret',
            }

            response = requests.post(token_url, data=data)
            respuesta = response.json()
            if response.status_code == 200:
                return respuesta.get('access_token')
            else:
                raise Exception(respuesta.get("error_description"))