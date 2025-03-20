#!/bin/bash

# Crear directorio para archivos estáticos
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput