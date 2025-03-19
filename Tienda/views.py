from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto,Boleta,detalle_boleta
from .forms import ProductoForm, RegistroUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
from Tienda.compra import Carrito
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def obtener_cantidad_total_carrito(request):
    carrito = request.session.get('carrito', {})
    cantidad_total = sum(item['cantidad'] for item in carrito.values())
    return cantidad_total

def subtotal(request):
    carrito = request.session.get('carrito', {})
    subtotal = sum(int(item['precio']) * item['cantidad'] for item in carrito.values())
    return subtotal


def mostrarInicio(request):
    productos = Producto.objects.all()

    datos={
        'productos':productos,
    }
    return render(request, 'inicio.html', datos)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    productos_relacionados = Producto.objects.filter(categoria=producto.categoria).exclude(idProducto=id)[:4]
    
    datos = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'producto_detalle.html', datos)

@login_required
def agregar_producto(request, id):
    carrito_compra = Carrito(request)
    producto = Producto.objects.get(idProducto = id)

    if producto.stock > 0:
        carrito_compra.agregar(producto=producto)
        
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Producto agregado al carrito',
                'cart_count': obtener_cantidad_total_carrito(request)
            })
        else:
            messages.success(request, "Producto agregado al carrito correctamente")
            return redirect('inicio')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'El producto está agotado'
            })
        else:
            messages.error(request, "El producto está agotado")
            return redirect('inicio')

def eliminar_producto(request, id):
    carrito_compra = Carrito(request)
    producto = Producto.objects.get(idProducto = id)
    carrito_compra.eliminar(producto=producto)
    return redirect('inicio')

def restar_producto(request, id):
    carrito_compra = Carrito(request)
    producto = Producto.objects.get(idProducto = id)
    carrito_compra.restar(producto=producto)
    return redirect('inicio')

@csrf_exempt
def limpiar_carrito(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Es una solicitud AJAX
        if request.method == 'POST':
            if 'carrito' in request.session:
                del request.session['carrito']
                request.session.modified = True
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    else:
        # Es una solicitud normal
        carrito_compra = Carrito(request)
        carrito_compra.limpiar()
        return redirect('inicio')

@login_required
def listarProductos(request):
    v_productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(v_productos, 3)
        v_productos = paginator.page(page)
    except:
        raise Http404

    datos = {
        'entity':v_productos,
        'paginator':paginator
    }
    return render(request, 'listarproductos.html', datos)

@login_required
def crearProductos(request):
    if request.method == "POST":
        productoform = ProductoForm(request.POST, request.FILES)
        if productoform.is_valid():
            productoform.save()
            messages.success(request, "Creado Correctamente")
            return redirect('listarProductos')
    else:
        productoform = ProductoForm()
    return render (request, 'crearproductos.html', {'productoform':productoform})

@login_required
def eliminarProductos(request, id):
    productoEliminado = Producto.objects.get(idProducto=id)
    productoEliminado.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect('listarProductos')

@login_required
def modificarProductos(request, id):
    productoMod = Producto.objects.get(idProducto=id) #buscar objeto
    datos = {
        'form':ProductoForm(instance=productoMod)
    }
    if request.method == "POST":
        formulario = ProductoForm(data=request.POST, instance=productoMod, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect ('listarProductos')
    return render(request, 'modificarproductos.html', datos)

def registrar(request):
    data={
        'form':RegistroUserForm()
    }
    if request.method == "POST":
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('inicio')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def generarBoleta(request):
    precio_total=0
    for key,value in request.session['carrito'].items():
        precio_total = precio_total + int(value['precio']) * int(value['cantidad'])
    boleta = Boleta(total = precio_total, usuario=request.user)
    boleta.save()
    productos = []
    for key, value in request.session['carrito'].items():
        producto = Producto.objects.get(idProducto = value['idProducto'])
        cant = value['cantidad']
        subtotal = cant * int(value['precio'])
        detalle = detalle_boleta(id_boleta = boleta, id_producto=producto, cantidad = cant, subtotal = subtotal)
        detalle.save()
        producto.stock -= cant
        producto.save()
        productos.append(detalle)
    datos={
        'productos':productos,
        'fecha':boleta.fechaCompra,
        'total':boleta.total,
        'nombre':boleta.usuario,
    }
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'detallecarrito.html', datos)

# Add these imports at the top of your file
from django.http import JsonResponse
import json

# Modify your add to cart view to handle AJAX
def agregar_al_carrito(request, producto_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX request
        producto = get_object_or_404(Producto, idProducto=producto_id)
        
        # Your existing cart logic here
        if 'carrito' not in request.session:
            request.session['carrito'] = {}
            
        carrito = request.session['carrito']
        
        if producto_id in carrito:
            carrito[producto_id]['cantidad'] += 1
        else:
            carrito[producto_id] = {
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else ''
            }
            
        request.session['carrito'] = carrito
        request.session.modified = True
        
        # Calculate cart count
        cart_count = sum(item['cantidad'] for item in carrito.values())
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })
    else:
        # Handle regular request (fallback)
        return redirect('inicio')

# Add a view to update quantity
@csrf_exempt
def actualizar_cantidad(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        producto_id = data.get('product_id')
        action = data.get('action')
        
        if 'carrito' not in request.session:
            return JsonResponse({'success': False})
            
        carrito = request.session['carrito']
        
        if producto_id in carrito:
            if action == 'increase':
                carrito[producto_id]['cantidad'] += 1
            elif action == 'decrease':
                if carrito[producto_id]['cantidad'] > 1:
                    carrito[producto_id]['cantidad'] -= 1
                else:
                    del carrito[producto_id]
                    
            request.session['carrito'] = carrito
            request.session.modified = True
            
            # Calculate subtotal and total
            subtotal = carrito[producto_id]['precio'] * carrito[producto_id]['cantidad'] if producto_id in carrito else 0
            total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
            cart_count = sum(item['cantidad'] for item in carrito.values())
            
            return JsonResponse({
                'success': True,
                'quantity': carrito[producto_id]['cantidad'] if producto_id in carrito else 0,
                'subtotal': subtotal,
                'total': total,
                'cart_count': cart_count
            })
            
    return JsonResponse({'success': False})

# Add a view to remove item from cart
@csrf_exempt
def eliminar_del_carrito(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        producto_id = data.get('product_id')
        
        if 'carrito' not in request.session:
            return JsonResponse({'success': False})
            
        carrito = request.session['carrito']
        
        if producto_id in carrito:
            del carrito[producto_id]
            request.session['carrito'] = carrito
            request.session.modified = True
            
            # Calculate total
            total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
            cart_count = sum(item['cantidad'] for item in carrito.values())
            
            return JsonResponse({
                'success': True,
                'total': total,
                'cart_count': cart_count
            })
            
    return JsonResponse({'success': False})

