#!/bin/bash

# Instalar dependencias
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Colectar archivos estáticos
python3 manage.py collectstatic --noinput --clear