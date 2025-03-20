#!/bin/bash

# Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Colectar archivos estáticos
python manage.py collectstatic --noinput --clear