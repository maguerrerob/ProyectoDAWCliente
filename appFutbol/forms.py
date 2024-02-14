from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .helper import helper

class BusquedaRecintoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaRecintoForm(forms.Form):
    nombre = forms.CharField(required=False)

    ubicacion = forms.CharField(required=False)
    
    telefono = forms.CharField(required=False)

class BusquedaAvanzadaDatosusuarioForm(forms.Form):
    descripcion = forms.CharField(required=False)
    POSICIONES = [
        ("GOA","Portero"),
        ("DEF","Defensa"),
        ("MID","Centrocampista"),
        ("STR", "Delantero")
    ]
    posicion = forms.MultipleChoiceField(choices=POSICIONES,
                                required=False,
                                widget=forms.CheckboxSelectMultiple())
    ubicacion = forms.CharField(required=False)

class BusquedaAvanzadaPartidoForm(forms.Form):
    ESTADO = [
        ("F", "Completo"),
        ("A", "Disponible")
    ]
    estado = forms.MultipleChoiceField(choices=ESTADO,
                                       required=False,
                                       initial="A",
                                       widget=forms.Select())
    ESTILO = [
        ("5", "Fútbol sala"),
        ("7", "Fútbol 7"),
        ("11", "Fútbol 11"),
    ]
    estilo = forms.MultipleChoiceField(choices=ESTILO,
                                       required=False,
                                       widget=forms.CheckboxSelectMultiple())


class PartidoForm(forms.Form):
    # horas_choices = [(f'{i}:00', f'{i}:00') for i in range(0, 24)]
    # hora = forms.ChoiceField(choices=horas_choices,
    #                         widget=forms.Select(),
    #                         label="Escoja una hora")
    ESTADO = [
        ("F", "Completo"),
        ("A", "Disponible")
    ]
    estado = forms.ChoiceField(choices=ESTADO, required=False)
    TIPO = [
        ("Pr", "Privada"),
        ("Pu", "Pública")
    ]
    tipo = forms.ChoiceField(choices=TIPO, required=False)
    ESTILO = [
        ("5", "Fútbol sala"),
        ("7", "Fútbol 7"),
        ("11", "Fútbol 11"),
    ]
    estilo = forms.ChoiceField(choices=ESTILO, required=False)
    
    def __init__(self, *args, **kwargs):
        super(PartidoForm, self).__init__(*args, **kwargs)

        clientesDisponibles = helper.obtener_clientes_select()
        self.fields["creador"] = forms.ChoiceField(
            choices=clientesDisponibles,
            widget=forms.Select,
            required=False)
        
        recintos = helper.obtener_recintos_select()
        self.fields["campo_reservado"] = forms.ChoiceField(
            choices=recintos,
            widget=forms.Select,
            required=False)
        

class RecintoForm(forms.Form):
    nombre = forms.CharField(required=False)
    ubicacion = forms.CharField(required=False)
    telefono = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(RecintoForm, self).__init__(*args, **kwargs)

        duenyosrecintos = helper.obtener_duenyosrecintos_select()
        self.fields["dueño_recinto"] = forms.ChoiceField(
            choices=duenyosrecintos,
            widget=forms.Select,
            required=False)
        
class DatosUsuarioForm(forms.Form):
    descripcion = forms.CharField(required=False)
    POSICION = [
        ("GOA","Portero"),
        ("DEF","Defensa"),
        ("MID","Centrocampista"),
        ("STR", "Delantero")
    ]
    posicion = forms.ChoiceField(choices=POSICION, required=False)
    ubicacion = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(DatosUsuarioForm, self).__init__(*args, **kwargs)

        clientesDisponibles = helper.obtener_clientes_select()
        self.fields["cliente"] = forms.ChoiceField(
            choices=clientesDisponibles,
            widget=forms.Select,
            required=False
        )
        
class DatosUsuarioPatchUbicacionForm(forms.Form):
    ubicacion = forms.CharField(required=True)