from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrarInicio, name='inicio'),
    path('actualizar_cantidad/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar_del_carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('detalle/<str:id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar/<str:id>/', views.agregar_producto, name='agregar_producto'),
    path('eliminar/<str:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('restar/<str:id>/', views.restar_producto, name='restar_producto'),
    path('listar/', views.listarProductos, name='listarProductos'),
    path('crear/', views.crearProductos, name='crearProductos'),
    path('modificar/<str:id>/', views.modificarProductos, name='modificarProductos'),
    path('eliminarProducto/<str:id>/', views.eliminarProductos, name='eliminarProductos'),
    path('registrar/', views.registrar, name='registrar'),
    path('generar_boleta/', views.generarBoleta, name='generarBoleta'),
    path('agregar_al_carrito/<str:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
]