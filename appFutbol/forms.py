from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

class BusquedaRecintoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaRecintoForm(forms.Form):
    nombre = forms.CharField(required=True)

    ubicacion = forms.CharField(required=True)
    
    telefono = forms.CharField(required=True)