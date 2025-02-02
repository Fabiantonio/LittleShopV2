from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto 
        fields = ['idProducto', 'nombre', 'precio', 'stock','categoria', 'imagen']
        labels ={
            'idProducto': 'idProducto',
            'nombre'    : 'Nombre',
            'precio'    : 'Precio',
            'stock'     : 'stock',
            'categoria' : 'Categoria',
            'imagen'    : 'Imagen'
        }
        widgets={
            'idProducto':forms.TextInput(
                attrs={
                    'placeholder':'Ingrese id del producto..',
                    'id': 'idproducto',
                    'class': 'form-control m-2',
                }
            ),
            'nombre':forms.TextInput(
                attrs={
                    'placeholder':'Ingrese nombre del producto..',
                    'id': 'nombre',
                    'class': 'form-control m-2',
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'placeholder':'Ingrese precio del producto..',
                    'id':'precio',
                    'class':'form-control m-2',
                }
            ),
            'stock': forms.NumberInput(
                attrs={
                    'placeholder':'Ingrese stock del producto..',
                    'id':'stock',
                    'class':'form-control m-2',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'placeholder':'Ingrese categoria del producto..',
                    'id':'categoria',
                    'class':'form-control m-2',
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class':'form-control',
                    'id'   : 'imagen'
                }
            )
        }