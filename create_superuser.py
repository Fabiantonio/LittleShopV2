import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleShop.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Desactivar temporalmente las validaciones de contraseña
from django.conf import settings
old_validators = settings.AUTH_PASSWORD_VALIDATORS
settings.AUTH_PASSWORD_VALIDATORS = []

try:
    # Eliminar usuario si ya existe
    if User.objects.filter(username='admin').exists():
        User.objects.filter(username='admin').delete()
        print('Usuario admin eliminado')
    
    # Crear superusuario
    user = User.objects.create_superuser('admin', 'admin@example.com', '1234')
    print(f'Superusuario {user.username} creado con éxito')
    
    # Verificar cuántos productos hay en la base de datos
    from Tienda.models import Producto
    productos = Producto.objects.all()
    print(f'Número de productos en la base de datos: {productos.count()}')
    
except Exception as e:
    print(f'Error: {e}')
finally:
    # Restaurar validaciones
    settings.AUTH_PASSWORD_VALIDATORS = old_validators