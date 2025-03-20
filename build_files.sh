#!/bin/bash

# Crear directorio para archivos estáticos
# Usar la ruta específica de Python proporcionada por Vercel
/opt/vercel/python3.9/bin/python -m pip install -r requirements.txt
/opt/vercel/python3.9/bin/python manage.py collectstatic --noinput