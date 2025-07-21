#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar collectstatic
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate