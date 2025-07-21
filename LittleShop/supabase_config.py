from supabase import create_client
from django.conf import settings
import os

# Inicializar el cliente de Supabase
supabase = create_client(
    supabase_url=os.getenv('SUPABASE_URL'),
    supabase_key=os.getenv('SUPABASE_KEY')
)