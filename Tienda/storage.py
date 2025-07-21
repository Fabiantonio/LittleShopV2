from django.conf import settings
from supabase import create_client, Client

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

def create_bucket_if_not_exists(bucket_name='product-images'):
    try:
        # Intentar crear el bucket
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

# Crear el bucket al importar el módulo
create_bucket_if_not_exists()