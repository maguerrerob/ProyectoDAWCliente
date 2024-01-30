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