from .views import obtener_cantidad_total_carrito,subtotal

def total_carrito(request):
    total = 0
    cantidad_total_carrito = obtener_cantidad_total_carrito(request) 
    total_precio = subtotal(request)
    if 'carrito' in request.session:
        try:
            for key,value in request.session['carrito'].items():
                total = total + (int(value['precio']))*(value['cantidad'])
                
        except KeyError:
            request.session['carrito']={}
            total = 0
    return {'total_carrito':int(total),
            'cantidad_productos': cantidad_total_carrito,
            'subtotal':total_precio,
            }