class Carrito:
    def __init__(self, request):
        self.session = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito=carrito

    def agregar(self, producto):
        if producto.idProducto not in self.carrito.keys():
            self.carrito[producto.idProducto]={
                "idProducto":producto.idProducto,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 1,
                "total": producto.precio,
                "imagen": producto.imagen.url,
            }
        else:
            for key, value in self.carrito.items():
                if key == producto.idProducto:
                    value["cantidad"] = value["cantidad"]+1
                    value["precio"] = producto.precio
                    value["total"] = value["total"]+producto.precio
                    break
        self.guardar_carrito()
        return "Producto agregado al carrito"

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified=True

    def eliminar(self, producto):
        id = producto.idProducto
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
        return "Producto eliminado del carrito"

    def restar (self, producto):
        for key, value in self.carrito.items():
            if key == producto.idProducto:
                value["cantidad"] = value["cantidad"]-1
                value["total"] = int(value["total"])-producto.precio
                if value ["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carrito()
        return "Cantidad actualizada"

    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified=True
        return "Carrito vaciado"