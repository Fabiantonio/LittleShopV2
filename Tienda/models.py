from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

# Create your models here.
    
class Categoria(models.Model):
    idCategoria     = models.IntegerField(primary_key=True, verbose_name="Id Categoria")
    nombreCategoria = models.CharField(max_length=50, verbose_name="Nombre de Categoria")

    def __str__(self):
        return self.nombreCategoria
    
class Producto(models.Model):
    idProducto   = models.CharField(primary_key=True, max_length=2,verbose_name="Id Producto")
    nombre       = models.CharField(max_length=50, verbose_name="Nombre")
    precio       = models.IntegerField(verbose_name="Precio")
    stock        = models.IntegerField(verbose_name="Stock", null=True)
    imagen       = models.ImageField(upload_to="imagenes", null=True, blank=True, verbose_name='Imagen')
    categoria    = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    descripcion  = models.TextField(verbose_name="Descripción", null=True, blank=True)
    especificaciones = models.TextField(verbose_name="Especificaciones", null=True, blank=True)
    fecha_creacion = models.DateTimeField(verbose_name="Fecha de creación", default=datetime.datetime.now)
    destacado    = models.BooleanField(default=False, verbose_name="Producto destacado")

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('detalle_producto', args=[str(self.idProducto)])
    
class Boleta(models.Model):
    id_boleta   = models.AutoField(primary_key=True)
    total       = models.BigIntegerField()
    fechaCompra = models.DateTimeField(blank=False, null=False, default=datetime.datetime.now)
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_boleta)
    
class detalle_boleta(models.Model):
    id_boleta           = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta   = models.AutoField(primary_key=True)
    id_producto         = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad            = models.IntegerField()
    subtotal            = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)