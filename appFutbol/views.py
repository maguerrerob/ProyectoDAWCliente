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
    return {'Authorization': 'Bearer '+env("TOKEN_CLIENTE"), "Content-Type": "application/json"}

def crear_cabecera_duenyorecinto():
    return {'Authorization': 'Bearer '+env("TOKEN_DUENYORECINTO"), "Content-Type": "application/json"}

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
        return render(request, 'recintos/busqueda_mejorada_api.html',{"recintos_mostrar":recintos})
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
                return render(request, 'recintos/busqueda_mejorada_api.html',
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


# CRUD Partido
# Create
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

# PUT
def partido_put(request, partido_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    partido = helper.obtener_partido(partido_id)
    formulario = PartidoForm(datosFormulario,
            initial={
                'estado': partido['estado'],
                'tipo': partido["tipo"],
                'estilo': partido["estilo"],
                'creador': partido['creador']['id'],
                'campo_reservado': partido['campo_reservado']['id']
            }
    )
    if (request.method == "POST"):
        try:
            formulario = PartidoForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
           
            response = requests.put(
                env("URL_API") + "partido/put/" + str(partido_id), headers=headers, data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                # Redirecciono al listado completo de recintos
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
                            'partidos/actualizar_put_api.html',
                            {"formulario":formulario,"partido":partido})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    return render(request, 'partidos/actualizar_put_api.html',{"formulario":formulario,"partido":partido})

# PATCH
def partido_patch_hora(request, partido_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    partido = helper.obtener_partido(partido_id)
    formulario = PartidoPatchHoraForm(datosFormulario,
            initial={
                'hora': partido['hora'],
                # 'campo_reservado': partido['campo_reservado']
            }
    )
    if (request.method == "POST"):
        try:
            formulario = PartidoPatchHoraForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
            response = requests.patch(
                env("URL_API") + 'partido/actualizar/hora/' + str(partido_id),
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
                            'partidos/patch_hora_api.html',
                            {"formulario":formulario,"partido":partido})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'partidos/patch_hora_api.html',{"formulario":formulario,"partido":partido})

# DELETE
def partido_eliminar(request, partido_id):
    try:
        headers = crear_cabecera_cliente()
        response = requests.delete(env("URL_API") + "partido/eliminar/" + str(partido_id), headers=headers)
        if(response.status_code == requests.codes.ok):
            return redirect("partidos_api_mejorada")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('partidos_api_mejorada')



# CRUD Recinto
# Create
def recinto_create(request):
    if (request.method == "POST"):
        try:
            formulario = RecintoForm(request.POST)
            headers =  {'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json"}
            datos = formulario.data.copy()
            
            response = requests.post(env("URL_API") + "recinto/create",
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("recintos_lista_api")
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
                            'recintos/create_api.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = RecintoForm(None)

    return render(request, 'recintos/create_api.html',{"formulario":formulario})

# No lo uso para redireccionar después en editar el recinto, sino que redirecciono al listado completo de recintos
def recinto_obtener(request,recinto_id):
    recinto = helper.obtener_recinto(recinto_id)
    return render(request, 'recintos/recinto_mostrar.html',{"recinto":recinto})

# PUT
def recinto_put(request, recinto_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    recinto = helper.obtener_recinto(recinto_id)
    formulario = RecintoForm(datosFormulario,
            initial={
                'nombre': recinto['nombre'],
                'ubicacion': recinto["ubicacion"],
                'telefono': recinto["telefono"],
                'dueño_recinto': recinto['dueño_recinto']['id']
            }
    )
    if (request.method == "POST"):
        try:
            formulario = RecintoForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
           
            response = requests.put(
                env("URL_API") + "recinto/put/" + str(recinto_id), headers=headers, data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                # Redirecciono al listado completo de recintos
                return redirect("recintos_lista_api")
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
                            'recintos/actualizar_put_api.html',
                            {"formulario":formulario,"recinto":recinto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    return render(request, 'recintos/actualizar_put_api.html',{"formulario":formulario,"recinto":recinto})

# PATCH
def recinto_patch_nombre(request, recinto_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    recinto = helper.obtener_recinto(recinto_id)
    formulario = RecintoPatchNombreForm(datosFormulario,
            initial={
                'nombre': recinto['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = RecintoPatchNombreForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
            response = requests.patch(
                env("URL_API") + 'recinto/actualizar/nombre/' + str(recinto_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("recintos_lista_api")
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
                            'recintos/patch_nombre_api.html',
                            {"formulario":formulario,"recinto":recinto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'recintos/patch_nombre_api.html',{"formulario":formulario,"recinto":recinto})


# DELETE
def recinto_eliminar(request, recinto_id):
    try:
        headers = crear_cabecera_cliente()
        response = requests.delete(env("URL_API") + "recinto/eliminar/" + str(recinto_id), headers=headers)
        if(response.status_code == requests.codes.ok):
            return redirect("recintos_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('recintos_lista_api')


# CRUD DatosUsuario
# Create
def datosusuario_create(request):
    if (request.method == "POST"):
        try:
            formulario = DatosUsuarioForm(request.POST)
            headers =  {'Authorization': 'Bearer '+env("TOKEN_CLIENTE"),
                        "Content-Type": "application/json"}
            datos = formulario.data.copy()
            response = requests.post(env("URL_API") + "datosusuario/create",
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("datos_usuario")
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
                            'datosusuario/create_api.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    else:
         formulario = DatosUsuarioForm(None)

    return render(request, 'datosusuario/create_api.html',{"formulario":formulario})

# PUT
def datosusuario_put(request, datosusuario_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    datosusuario = helper.obtener_datosusuario(datosusuario_id)
    formulario = DatosUsuarioForm(datosFormulario,
            initial={
                'descripcion': datosusuario['descripcion'],
                'posicion': datosusuario["posicion"],
                'ubicacion': datosusuario["ubicacion"],
                'cliente': datosusuario['cliente']['id']
            }
    )
    if (request.method == "POST"):
        try:
            formulario = DatosUsuarioForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
           
            response = requests.put(
                env("URL_API") + "datosusuario/put/" + str(datosusuario_id), headers=headers, data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                # Redirecciono al listado completo de datos de usuarios
                return redirect("datos_usuario")
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
                            'datosusuario/actualizar_put_api.html',
                            {"formulario":formulario,"datosusuario":datosusuario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    return render(request, 'datosusuario/actualizar_put_api.html',{"formulario":formulario,"datosusuario":datosusuario})

# PATCH
def datosusuario_ubicacion(request, datosusuario_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    datosusuario = helper.obtener_datosusuario(datosusuario_id)
    formulario = DatosUsuarioPatchUbicacionForm(datosFormulario,
            initial={
                'ubicacion': datosusuario['ubicacion'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = DatosUsuarioPatchUbicacionForm(request.POST)
            headers = crear_cabecera_cliente()
            datos = request.POST.copy()
            response = requests.patch(
                env("URL_API") + 'datosusuario/actualizar_ubicacion/ubicacion/' + str(datosusuario_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("datos_usuario")
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
                            'datosusuario/patch_ubicacion_api.html',
                            {"formulario":formulario,"datosusuario":datosusuario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'datosusuario/patch_ubicacion_api.html',{"formulario":formulario,"datosusuario":datosusuario})


# DELETE
def datosusuario_eliminar(request, datosusuario_id):
    try:
        headers = crear_cabecera_cliente()
        response = requests.delete(env("URL_API") + "datosusuario/eliminar/" + str(datosusuario_id), headers=headers)
        if(response.status_code == requests.codes.ok):
            return redirect("datos_usuario")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('datos_usuario')


#----Registro----
def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {"Content-Type": "application/json"}
                response = requests.post(env("URL_API") + 'registrar/usuario', headers=headers, data=json.dumps(formulario.cleaned_data))
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    return redirect("index")
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
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

#----Login----
def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer ' + token_acceso} 
            response = requests.get(env("URL_API") + 'usuario/token/' + token_acceso, headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()

    return render(request, 'registration/login.html', {'form': formulario})

#----Logout----
def logout(request):
    del request.session['token']
    return redirect('index')

# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)