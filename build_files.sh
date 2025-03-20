#!/bin/bash

# Crear directorio para archivos estáticos
pip install -r requirements.txt
python manage.py collectstatic --noinput