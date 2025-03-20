import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleShop.settings')
django.setup()

from Tienda.models import Categoria, Producto
from django.core.files.images import ImageFile
from pathlib import Path

# Función para crear categorías si no existen
def crear_categorias():
    categorias = [
        {'idCategoria': 1, 'nombreCategoria': 'Perros'},
        {'idCategoria': 2, 'nombreCategoria': 'Gatos'},
        {'idCategoria': 3, 'nombreCategoria': 'Aves'},
        {'idCategoria': 4, 'nombreCategoria': 'Accesorios'}
    ]
    
    for cat in categorias:
        Categoria.objects.get_or_create(
            idCategoria=cat['idCategoria'],
            defaults={'nombreCategoria': cat['nombreCategoria']}
        )
    print(f'Categorías creadas: {Categoria.objects.count()}')

# Función para crear productos
def crear_productos():
    # Verificar si ya hay productos
    if Producto.objects.count() > 0:
        print('Ya existen productos en la base de datos')
        return
    
    # Obtener categorías
    categorias = Categoria.objects.all()
    if not categorias.exists():
        print('No hay categorías. Creando categorías primero...')
        crear_categorias()
        categorias = Categoria.objects.all()
    
    # Lista de productos
    productos = [
        {
            'idProducto': '01', 
            'nombre': 'Casa para perro', 
            'precio': 25000, 
            'stock': 10,
            'imagen': 'dog_house.png',
            'categoria': 1,
            'descripcion': 'Casa cómoda para tu perro',
            'destacado': True
        },
        {
            'idProducto': '02', 
            'nombre': 'Hueso de juguete', 
            'precio': 5000, 
            'stock': 20,
            'imagen': 'hueso_dog.png',
            'categoria': 1,
            'descripcion': 'Juguete resistente para perros',
            'destacado': False
        },
        {
            'idProducto': '03', 
            'nombre': 'Plato para perro', 
            'precio': 8000, 
            'stock': 15,
            'imagen': 'plato_dog.png',
            'categoria': 1,
            'descripcion': 'Plato de acero inoxidable para perros',
            'destacado': False
        },
        {
            'idProducto': '04', 
            'nombre': 'Collar con púas', 
            'precio': 12000, 
            'stock': 8,
            'imagen': 'collar_puas.png',
            'categoria': 1,
            'descripcion': 'Collar decorativo para perros',
            'destacado': False
        },
        {
            'idProducto': '05', 
            'nombre': 'Juguete para gato', 
            'precio': 4500, 
            'stock': 25,
            'imagen': 'cat_toy.png',
            'categoria': 2,
            'descripcion': 'Juguete interactivo para gatos',
            'destacado': True
        },
        {
            'idProducto': '06', 
            'nombre': 'Túnel para gato', 
            'precio': 15000, 
            'stock': 7,
            'imagen': 'tunel_cat.png',
            'categoria': 2,
            'descripcion': 'Túnel plegable para gatos',
            'destacado': False
        },
        {
            'idProducto': '07', 
            'nombre': 'Comida Whiskas', 
            'precio': 9000, 
            'stock': 30,
            'imagen': 'whiskas_img.png',
            'categoria': 2,
            'descripcion': 'Alimento premium para gatos',
            'destacado': True
        },
        {
            'idProducto': '08', 
            'nombre': 'Jaula para pájaros', 
            'precio': 35000, 
            'stock': 5,
            'imagen': 'jaula_pajaro.png',
            'categoria': 3,
            'descripcion': 'Jaula espaciosa para aves pequeñas',
            'destacado': True
        },
        {
            'idProducto': '09', 
            'nombre': 'Comida para pájaros', 
            'precio': 6000, 
            'stock': 40,
            'imagen': 'comida_pajaro.png',
            'categoria': 3,
            'descripcion': 'Mezcla de semillas para aves',
            'destacado': False
        },
        {
            'idProducto': '10', 
            'nombre': 'Bebedero para mascotas', 
            'precio': 7500, 
            'stock': 18,
            'imagen': 'pet_water.png',
            'categoria': 4,
            'descripcion': 'Bebedero automático para mascotas',
            'destacado': False
        },
        {
            'idProducto': '11', 
            'nombre': 'Transportadora', 
            'precio': 28000, 
            'stock': 12,
            'imagen': 'pet_cage.png',
            'categoria': 4,
            'descripcion': 'Transportadora segura para mascotas',
            'destacado': True
        },
    ]
    
    # Crear productos
    for prod in productos:
        # Obtener la categoría
        categoria = Categoria.objects.get(idCategoria=prod['categoria'])
        
        # Verificar si la imagen existe
        imagen_path = Path('files/imagenes') / prod['imagen']
        if not imagen_path.exists():
            print(f'Advertencia: Imagen {prod['imagen']} no encontrada')
            imagen = None
        else:
            imagen = f"imagenes/{prod['imagen']}"
        
        # Crear el producto
        producto, created = Producto.objects.get_or_create(
            idProducto=prod['idProducto'],
            defaults={
                'nombre': prod['nombre'],
                'precio': prod['precio'],
                'stock': prod['stock'],
                'imagen': imagen,
                'categoria': categoria,
                'descripcion': prod['descripcion'],
                'destacado': prod['destacado']
            }
        )
        
        if created:
            print(f"Producto creado: {producto.nombre}")
        else:
            print(f"Producto ya existía: {producto.nombre}")

# Ejecutar funciones
if __name__ == '__main__':
    try:
        print("Creando categorías...")
        crear_categorias()
        
        print("\nCreando productos...")
        crear_productos()
        
        print(f"\nTotal de productos en la base de datos: {Producto.objects.count()}")
    except Exception as e:
        print(f"Error: {e}")