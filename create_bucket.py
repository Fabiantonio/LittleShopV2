import os
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleShop.settings')
django.setup()

# Importar después de configurar Django
from supabase import create_client, Client

# Crear cliente de Supabase
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def create_bucket_if_not_exists(bucket_name='product-images'):
    try:
        # Intentar crear el bucket usando createBucket
        supabase.storage.createBucket(
            bucket_name,
            {'public': True}
        )
        print(f'Bucket {bucket_name} creado exitosamente')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'El bucket {bucket_name} ya existe')
        else:
            print(f'Error al crear el bucket: {str(e)}')
            
        # Intentar listar los buckets existentes
        try:
            buckets = supabase.storage.listBuckets()
            print('\nBuckets existentes:')
            for bucket in buckets:
                print(f'- {bucket["name"]}')
        except Exception as e:
            print(f'Error al listar buckets: {str(e)}')

if __name__ == '__main__':
    create_bucket_if_not_exists()